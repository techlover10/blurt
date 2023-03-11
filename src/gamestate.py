
import sqlite3
import asyncio
import json
import random
import time

import sys
import importlib
def reload():
    importlib.reload(sys.modules[__name__])


MAX_TIER = 3
MAX_PING = 3000


class GameRunner():
    def __init__(self, cm, dbfile):
        self.cm = cm # the connection manager, for broadcast mostly
        self.dbc = sqlite3.connect(dbfile) # idk the path to the words database
        # prolly not an efficient way of doing this (for db), but queries are pretty rare tbqh
        self.maxVal = 3 # potentially alterable

        self.notLive = True
        self.currWord = None
        self.currVal = 0
        self.players = {}
        self.pingTime = None
        self.ansTime = None
    def get_player(self, msg):
        if 'user' not in msg:
            return None
        u = msg['user']
        if u not in self.players:
            return None
        p = self.players[u]
        return p
    def generate_question(self):
        # assuming roll is same as tier for now
        self.currVal = random.randint(1,self.maxVal)
        self.skips = 0
        tier = self.currVal
        cur = self.dbc.cursor()
        params = (tier,)
        res = cur.execute("SELECT * FROM clues WHERE tier = ? ORDER BY random() LIMIT 1", params).fetchone()
        self.currWord = res[2]
        # return res.fetchone()
        for p in self.players.values():
            p.skip = False
        if self.cm is not None:
            self.pingTime = time.time_ns() // 1000
            self.ansTime = None
            self.notLive = False
            msgobj = {'type': 'clue', 'clue': res[3], 'value': self.currVal}
            #asyncio.run(self.cm.broadcast(json.dumps(msgobj)))
            return msgobj
    def end_round(self):
        # sends the scores
        self.notLive = True
        scores = []
        for p in self.players.values():
            p.ready = False
            scores.append({'name': p.name, 'score': p.score})
        obj = {'type': 'end', 'scores': scores, 'answer': self.currWord}
        #await self.cm.broadcast(json.dumps(obj))
        return obj
    def emptier(self):
        # essentially a soft reset
        print("emptying")
        self.notLive = True
        self.currWord = None
        self.currVal = 0
        self.players = {}
        self.pingTime = None
        self.ansTime = None
    async def dispatch(self, msg, ws, cmgr):
        print("in dispatch with ", msg)
        if 'join' in msg:
            name = msg['join']
            if name not in self.players:
                pl = Player(name)
                self.players[name] = pl
                o = pl.obj()
                o['type'] = 'join'
                #asyncio.run(self.cm.broadcast(json.dumps(o)))
                plrs = [p.obj() for p in self.players.values()]
                po = {'scores': plrs, 'type': 'scores'}
                #await ws.send(json.dumps(po))
                po2 = {'type':'reg'}
                await ws.send(json.dumps(po2))
                await self.cm.broadcast(json.dumps(po))
        elif 'skip' in msg:
            if self.notLive:
                return
            # yeah i guess else makes sense here, keep messages from client simple
            player = self.get_player(msg)
            if player is None:
                return
            player.skip = True
            for p in self.players.values():
                if not p.skip:
                    return
            # what to do if all skip? end the round
            obj = self.end_round()
            await self.cm.broadcast(json.dumps(obj))
        elif 'pong' in msg:
            if self.notLive:
                return
            p = self.get_player(msg)
            if p is None:
                return
            t = time.time_ns() // 1000
            p.ping = min(t - self.pingTime, MAX_PING) # max 3 seconds
        elif 'guess' in msg:
            if self.notLive:
                return
            p = self.get_player(msg)
            if p is None:
                return
            p.guess = msg['guess']
            if p.skip: # am I sure that i want this?
                return # given up their right to guess
            if p.guess == self.currWord:
                ct = time.time_ns() // 1000
                if self.ansTime is None:
                    p.score += self.currVal
                    self.ansTime = ct
                    # have to trigger and end round in a few secs
                    await asyncio.sleep(5)
                    #await self.end_round()
                    obj = self.end_round()
                    await self.cm.broadcast(json.dumps(obj))
                    # does any of this even work lol?
                elif ct - self.ansTime < p.ping:
                    p.score += self.currVal
            # now send to everyone
            o = {'guess': msg['guess'], 'type': 'guess', 'name': p.name}
            await asyncio.sleep(0.5)
            await self.cm.broadcast(json.dumps(o))
        elif 'ready' in msg:
            if not self.notLive:
                print('not ready')
                return
            p = self.get_player(msg)
            print('player ', p)
            if p is None:
                return
            p.ready = True
            for pl in self.players.values():
                if not pl.ready:
                    return
            # now everyone ready, time for a new round
            q = self.generate_question()
            print(q)
            await self.cm.broadcast(json.dumps(q))
        elif 'leave' in msg:
            # this guy is for me to make people leave or whatever
            p = self.get_player(msg)
            self.players.pop(p.name)
        elif 'clear' in msg:
            self.emptier()
        elif 'forceready' in msg:
            q = self.generate_question()
            await self.cm.broadcast(json.dumps(q));
            
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.ping = MAX_PING
        self.guess = None
        self.skip = False
        self.ready = False
    def obj(self):
        return {'name': self.name, 'score': self.score}
