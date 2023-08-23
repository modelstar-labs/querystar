import json
import click
import asyncio
import requests
import websockets
from websockets.client import WebSocketClientProtocol
from querystar.settings import settings


class ClientConnection:
    def __init__(self, integration: str, event: str, client_id: str):
        self.integration = integration
        self.event = event
        self.client_id = client_id

    @staticmethod
    async def _trigger(ws_client_url: str, filter_function: callable = None, filter_params: dict = {}):
        async with websockets.connect(ws_client_url) as websocket:
            headers_send = {
                "Authorization": f"Bearer {settings.querystar_token}"}
            await websocket.send(json.dumps(headers_send))
            # async for message in websocket:
            #     print("Demo Socket", message)
            #     await websocket.close()
            while True:
                _r = await websocket.recv()
                try:
                    _data = json.loads(_r)
                except:
                    _data = _r
                if isinstance(_data, str) and _data == 'Unauthorized trigger subscription.':
                    raise Exception('Unauthorized trigger subscription.')
                if _data:
                    if filter_function and isinstance(_data, dict):
                        if filter_function(_data, filter_params):
                            return _data
                        else:
                            continue
                    # await websocket.close() # not needed within context manager
                    else:
                        return _data

    def listen(self, params: dict = {}, filter_function: callable = None, filter_params: dict = {}):
        _host = settings.querystar_server_host
        _ssl = settings.ssl
        _route = f"client/trigger/{self.integration}/{self.event}/{self.client_id}"
        if _ssl:
            _ws_client_url = f"wss://{_host}/{_route}"
        else:
            _ws_client_url = f"ws://{_host}/{_route}"
        data = asyncio.run(self._trigger(
            _ws_client_url, filter_function, filter_params))
        return data

    def fire(self, payload: dict = {}):
        headers = {
            'Authorization': f'Bearer {settings.querystar_token}',
            'Content-type': 'application/json'
        }
        _host = settings.querystar_server_host
        _ssl = settings.ssl
        _route = f"client/action/{self.integration}/{self.event}/{self.client_id}"
        if _ssl:
            _http_client_url = f"https://{_host}/{_route}"
        else:
            _http_client_url = f"http://{_host}/{_route}"

        data = requests.post(
            _http_client_url, headers=headers, data=json.dumps(payload))
        json_data = data.json()
        return json_data
