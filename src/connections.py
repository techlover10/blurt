
import asyncio
import websockets
import json

import sqlite3

import sys
import importlib
def reload():
    importlib.reload(sys.modules[__name__])


connections = set()

currGame = None

class ConnectionManager:
    def __init__(self, dispatch=None, emptier=None, leaver=None):
        self.id_counter = 0
        if dispatch:
            self.df = dispatch
            self.emptier = emptier # this is when there's nobody left in the room...
            self.leaver = leaver
        else:
            def emptydf(x,y):
                pass
            self.df = emptydf
        self.connections = set()
    async def _start_server(self):
        async with websockets.serve(self.register, "localhost", 8765):
            await asyncio.Future()
    def start_server(self):
        asyncio.run(self._start_server())
    async def dispatch(self,msg,ws):
        if self.df:
            await self.df(msg, ws, self)
    async def consumer(self, ws):
        async for message in ws:
            jm = json.loads(message)
            await self.dispatch(jm, ws)
            # await self.broadcast(json.dumps(jm)) # do i want this last one for debug? phaps
    async def producer(self, ws):
        # pls don't use
        while True:
            msg = await dumbprod()
            await ws.send(msg)
    async def register(self,ws):
        print("new reg")
        self.id_counter += 1
        ws._cm_id = self.id_counter
        print(ws)
        #print(dir(ws))
        self.connections.add(ws)
        asyncio.gather(
            self.consumer(ws)
        )
        try:
            await ws.wait_closed()
        finally:
            print("drop conn")
            old_id = ws._cm_id
            await self.leaver(old_id)
            self.connections.remove(ws)
            if not self.connections: # kinda hate this... `not <set>` is same as empty check...
                self.emptier()
    async def broadcast(self,msg):
        websockets.broadcast(self.connections, msg)


async def dumbprod():
    await asyncio.sleep(10)
    yield "prod"

async def dispatch(ws):
    async for message in ws:
        print(message)
        await ws.send('pong')

async def register(ws):
    connections.add(ws)
    try:
        await websocket.wait_closed()
    finally:
        connections.remove(ws)

async def main():
    async with websockets.serve(dispatch, "localhost", 8765):
        await asyncio.Future()




#asyncio.run(main())
