from asyncio import sleep, get_event_loop
from aiohttp import ClientSession
from typing import OrderedDict, Union, List

from numpy.random import randint
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from services import json_dumps, json_loads


class RequestRpc:
    REFRESH_TOKEN_TIME = 30*60  # in sec

    def __init__(self, url: str, username: str, password: str, token_url: str, ):
        self.url = url
        self.username = username
        self.password = password
        self.token_url = token_url
        self._oauth = OAuth2Session(client=LegacyApplicationClient(client_id=username))
        self._token = None
        self._token_refresh_task = get_event_loop().create_task(self.refresh_token_loop())
        self._session = None

    async def refresh_token_loop(self):
        while True:
            try:
                await self.refresh_token()
            except Exception as err:
                pass
            await sleep(self.REFRESH_TOKEN_TIME)

    async def refresh_token(self):
        self._token = self._oauth.fetch_token(
            token_url=self.token_url,
            username=self.username,
            password=self.password
        )

    async def rpc_request(self, methods: Union[OrderedDict, List[str], str]):
        if not self._token:
            await self.refresh_token()

        if isinstance(methods, OrderedDict):
            body = [{
                "jsonrpc": "2.0",
                "method": m,
                "params": v or dict(),
                "id": randint(10000000)
            } for m, v in methods.items()]
        elif isinstance(methods, List):
            body = [{
                "jsonrpc": "2.0",
                "method": m,
                "id": randint(10000000)
            } for m in methods]
        elif isinstance(methods, str):
            body = [{
                "jsonrpc": "2.0",
                "method": methods,
                "id": randint(10000000)
            }]
        else:
            raise Exception('Unexpected type params.')

        if not self._session:
            self._session = ClientSession(json_serialize=json_dumps)

        for i in range(4):
            async with self._session.get(self.url+'authentication_check', headers=self._prepare_headers()) as resp:
                if resp.status == 200:
                    results = await resp.json(loads=json_loads)
                    if results.get('Status') == 'OK':
                        break
                await sleep(5**i)
                await self.refresh_token()
                continue

        async with self._session.post(self.url, headers=self._prepare_headers(), json=body) as resp:
            results = await resp.json(loads=json_loads)

            for result in results:
                if 'error' in result:
                    raise Exception(result['error'].get('message'))

        if isinstance(methods, str):
            return results[0]

        return results

    def _prepare_headers(self):
        headers = {
            'Authorization': f'{self._token["token_type"]} {self._token["access_token"]}',
            'Content-Type': 'application/json'
        }
        return headers
