
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
    def __init__(self, dispatch=None):
        if dispatch:
            self.df = dispatch
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
    def dispatch(self,msg,ws):
        self.df(msg, ws, self)
    async def consumer(self, ws):
        async for message in ws:
            jm = json.loads(message)
            print(jm)
            if 'join' in jm:
                print("joined: ", jm['join'])
            self.dispatch(jm, ws)
            await self.broadcast(json.dumps(jm))
    async def producer(self, ws):
        # pls don't use
        while True:
            msg = await dumbprod()
            await ws.send(msg)
    async def register(self,ws):
        print("new reg")
        print(ws)
        self.connections.add(ws)
        asyncio.gather(
            self.consumer(ws)
        )
        try:
            await ws.wait_closed()
        finally:
            print("drop conn")
            self.connections.remove(ws)
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
