import asyncio
import asyncws
import json
from pprint import pprint
import requests


def parse_state_json(json_data):
    try:
        json_data = json.loads(json_data)
        data = json_data['event']['data']
        entity_id = data['entity_id']
        name = data['new_state']['attributes']['friendly_name']
        if name in ('Red', 'Blue', "Green"):
            new_state = data['new_state']['state']
            print(name)
            print(new_state)
            if name == "Red":
                entity_id = "binary_sensor.tv"
                url = f'http://127.0.0.1:5000/change-state/{entity_id}/{new_state}'
                requests.get(url)
            if name == "Blue":
                entity_id = "binary_sensor.kitchen_window"
                url = f'http://127.0.0.1:5000/change-state/{entity_id}/{new_state}'
                requests.get(url)
            if name == "Green":
                entity_id = "binary_sensor.power_stri"
                url = f'http://127.0.0.1:5000/change-state/{entity_id}/{new_state}'
                requests.get(url)
    except Exception as e:
        pass

@asyncio.coroutine
def echo():
    websocket = yield from asyncws.connect('ws://172.16.230.225:8123/api/websocket')

    yield from websocket.send(json.dumps({"type": "auth", "api_password": "tokyocommit"}))
    yield from websocket.send(json.dumps({'id': 1, 'type': 'subscribe_events', }))
    while True:
        message = yield from websocket.recv()
        if message is None:
            break
        # print(message)
        parse_state_json(message)

asyncio.get_event_loop().run_until_complete(echo())
asyncio.get_event_loop().close()
