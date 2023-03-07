
import sqlite3
import asyncio
import json
import random

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
    def generate_question(self):
        # assuming roll is same as tier for now
        self.currVal = random.randint(1,self.maxVal)
        self.skips = 0
        tier = currVal
        cur = self.dbc.cursor()
        params = (tier,)
        res = cur.execute("SELECT * FROM clues WHERE tier = ? ORDER BY random() LIMIT 1", params)
        self.currWord = res[2]
        # return res.fetchone()
        if self.cm is not None:
            self.pingTime = time.time_ns() // 1000
            self.ansTime = None
            self.notLive = False
            msgobj = {type: 'clue', clue: res[3]}
            asyncio.run(self.cm.broadcast(json.dumps(msgobj)))
    def end_round(self):
        # sends the scores
        self.notLive = True
        scores = []
        for p in self.players.values():
            scores.append({p.name: p.score})
        obj = {type: 'end', scores: scores, answer: self.currWord}
        asyncio.run(self.cm.broadcast(json.dumps(obj)))
    def dispatch(self, msg, ws, cmgr):
        if 'join' in msg:
            name = msg['join']
            if name not in self.players:
                pl = Player(name)
                self.players[name] = pl
                o = pl.obj()
                o['type'] = 'join'
                asyncio.run(self.cm.broadcast(json.dumps(o)))
        elif 'skip' in msg:
            if self.notLive:
                return
            # yeah i guess else makes sense here, keep messages from client simple
            if 'user' not in msg:
                return
            name = msg['user']
            player = self.players[name]
            if player:
                player.skip = True
            for p in self.players.values():
                if not p.skip:
                    return
            # what to do if all skip? end the round
            self.end_round(True)
        elif 'pong' in msg:
            if self.notLive:
                return
            if 'user' not in msg:
                return
            u = msg['user']
            if u not in self.players:
                return
            p = self.players[u]
            t = time.time_ns() // 1000
            p.ping = min(t - self.pingTime, MAX_PING) # max 3 seconds
        elif 'guess' in msg:
            if self.notLive:
                return
            if 'user' not in msg:
                return
            u = msg['user']
            if u not in self.players:
                return
            p = self.players[u]
            p.guess = msg['guess']
            if p.skip:
                return # given up their right to guess
            if p.guess == self.currWord:
                ct = time.time_ns() // 1000
                if self.ansTime is None:
                    self.ansTime = ct
                    # have to trigger and end round in a few secs
                    asyncio.wait(self.end_round, timeout=5)
                    # does any of this even work lol?
                elif ct - self.ansTime < p.ping:
                    p.score += self.currVal
                    
class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.ping = MAX_PING
        self.guess = None
        self.skip = False
    def obj(self):
        return {'name': self.name, 'score': self.score}
