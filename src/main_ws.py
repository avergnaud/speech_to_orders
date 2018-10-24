'''
serveur websocket

ATTENTION : il faut lancer un client (client.py) pour que ça fonctionne

"connecte-toi"
"branche-toi sur Kraken"
"exit Kraken"
"sors de Kraken"

'''
import asyncio
import websockets
from main import listen_for_speech


async def hello(websocket, path):
   for value in listen_for_speech():
       await websocket.send(value)
       print("envoyé")


if __name__ == '__main__' :
    # listen_for_speech()  # listen to mic.
    start_server = websockets.serve(hello, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()