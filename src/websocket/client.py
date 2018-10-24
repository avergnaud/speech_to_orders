'''
client websocket
'''
import asyncio
import websockets

async def hello():
   async with websockets.connect(
           'ws://localhost:8765/') as websocket:
       while True:
           received = await websocket.recv()
           print(received)

asyncio.get_event_loop().run_until_complete(hello())