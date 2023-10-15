from rich.console import Console
import asyncio
import websockets

console = Console()

async def handler(websocket):
    while True:
        payload = await websocket.recv()
        await websocket.send(payload)        

async def main():
    async with websockets.serve(handler, "", 8001):
        print('ws://localhost:8001')
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())