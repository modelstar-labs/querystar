import time
import json
import click
import asyncio
import requests
import websockets
from uuid import uuid4
from websockets.client import WebSocketClientProtocol
from querystar.settings import settings


class TriggerEventList:
    def __init__(self):
        self._event_list: dict[str, list] = {}
        self._event_pointers: list[str] = []

    @property
    def display(self) -> str:
        _str = ''
        for key, value in self._event_list.items():
            _str = _str + f'{key}: {len(value)} :: '
        return _str

    def init_trigger_event(self, event_pointer: str):
        self._event_list[event_pointer] = []
        self._event_pointers.append(event_pointer)
        print(f'Initialized trigger event {event_pointer}')

    def trigger_event(self, event_pointer: str, data: dict):
        self._event_list[event_pointer].append(data)
        print(f'Triggered event {event_pointer} to {len(self._event_list[event_pointer])} items')

    def is_trigger_initialized(self, event_pointer: str) -> bool:
        return event_pointer in self._event_pointers


_event_list = TriggerEventList()


class ClientConnection:
    def __init__(self, event_list: TriggerEventList):
        self.client_id = str(uuid4())
        self._local_event_list: TriggerEventList = event_list

    @staticmethod
    async def _trigger(event_list: TriggerEventList,
                       ws_client_url: str,
                       trigger_pointer: str,
                       filter_function: callable = None,
                       filter_params: dict = {}) -> dict:

        async with websockets.connect(ws_client_url) as websocket:
            headers_send = {
                "Authorization": f"Bearer {settings.querystar_token}"}
            await websocket.send(json.dumps(headers_send))
            # async for message in websocket:
            #     print("Demo Socket", message)
            #     await websocket.close()
            while True:
                print(event_list.display)
                _r = await websocket.recv()
                try:
                    _data = json.loads(_r)
                    print('Recieved trigger event')
                except:
                    _data = _r
                if isinstance(_data, str) and _data == 'Unauthorized trigger subscription.':
                    raise Exception('Unauthorized trigger subscription.')
                if _data:
                    if filter_function and isinstance(_data, dict):
                        if filter_function(_data, filter_params):
                            # return _data
                            print('Gone through filter function')
                            event_list.trigger_event(trigger_pointer, _data)
                        else:
                            print('Rejected by filter function')
                            continue
                    # await websocket.close() # not needed within context manager
                    else:
                        # return _data
                        print('Gone through no filter function')
                        event_list.trigger_event(trigger_pointer, _data)

    def listen(self,
               integration: str,
               event: str,
               params: dict = {},
               filter_function: callable = None,
               filter_params: dict = {}) -> dict:
        _trigger_pointer = f'{integration}/{event}/{self.client_id}'
        while True:
            if not self._local_event_list.is_trigger_initialized(_trigger_pointer):
                self._local_event_list.init_trigger_event(_trigger_pointer)
                _host = settings.querystar_server_host
                _ssl = settings.ssl
                _route = f"client/trigger/{integration}/{event}/{self.client_id}"
                if _ssl:
                    _ws_client_url = f"wss://{_host}/{_route}"
                else:
                    _ws_client_url = f"ws://{_host}/{_route}"
                # TODO: this is blocking, so make it run on a separate thread, and clean it up when done
                print('running trigger 0')
                asyncio.run(self._trigger(self._local_event_list,
                                          _ws_client_url,
                                          _trigger_pointer,
                                          filter_function,
                                          filter_params))
                print('running trigger 1')
            else:
                # TODO: check for empty lists, ACID, racing conditions
                print(
                    f'{self._local_event_list[_trigger_pointer]} len of event list')
                if len(self._local_event_list[_trigger_pointer]) > 0:
                    data = self._local_event_list[_trigger_pointer].pop(0)
                    return data
                else:
                    time.sleep(0.5)
                    continue

    def setup_trigger(self,
                      integration: str,
                      event: str,
                      params: dict = {},
                      filter_function: callable = None,
                      filter_params: dict = {}) -> dict:

        pass

    def fire(self, integration: str, event: str, payload: dict = {}) -> dict:
        headers = {
            'Authorization': f'Bearer {settings.querystar_token}',
            'Content-type': 'application/json'
        }
        _host = settings.querystar_server_host
        _ssl = settings.ssl
        _route = f"client/action/{integration}/{event}/{self.client_id}"
        if _ssl:
            _http_client_url = f"https://{_host}/{_route}"
        else:
            _http_client_url = f"http://{_host}/{_route}"

        data = requests.post(
            _http_client_url, headers=headers, data=json.dumps(payload))
        json_data = data.json()
        return json_data


_client_connection = ClientConnection(event_list=_event_list)
