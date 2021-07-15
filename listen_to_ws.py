import asyncio
import websockets
import json

async def recieve(websocket):
    msg = await websocket.recv()
    msg = json.loads(msg)
    return msg
async def send(websocket):
    await websocket.send(json.dumps({'Luz_1': 'cambio'}))
    await asyncio.sleep(1)
async def use_ws():
    uri = "ws://localhost:8000/ws/test/"
    while True: 
        try:
            async with websockets.connect(uri) as websocket:
                while True: 
                    await send(websocket)
                    msg = await recieve(websocket)
                    print(msg)
        except:
            await asyncio.sleep(0.1)


asyncio.run(use_ws())


                