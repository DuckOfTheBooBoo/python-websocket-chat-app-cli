from rich.prompt import Prompt
from rich.console import Console
from datetime import datetime
import asyncio
import aioconsole
import websockets
import json

console = Console()

NAME = ''
TIME_FORMAT = '%d/%m/%y - %H:%M:%S'

def print_payload(payload: dict):
    payload_datetime = datetime.strptime(payload['time'], TIME_FORMAT)
    time = payload_datetime.strftime('%H:%M')

    console.print(f'[yellow]{payload["sender"]}[/] ({time}): {payload["message"]}')

async def receive_msg(websocket):
    while True:
        incoming_payload = await websocket.recv()
        payload = json.loads(incoming_payload)
        print_payload(payload)
        

async def websocket_client(server_uri):
    async with websockets.connect(server_uri) as websocket:

        asyncio.create_task(receive_msg(websocket))

        while True:
            line = await aioconsole.ainput('\rYou: \r')
            now = datetime.now().strftime(TIME_FORMAT)
            payload = {
                'sender': NAME,
                'time': now,
                'message': line
            }
            print_payload(payload)
            # Stringify payload
            serialized_payload = json.dumps(payload)
            await websocket.send(serialized_payload)

if __name__ == '__main__':
    # server_uri = Prompt.ask('Server URI')
    NAME = Prompt.ask('Whats your name')

    asyncio.get_event_loop().run_until_complete(websocket_client('ws://localhost:8001'))
    
