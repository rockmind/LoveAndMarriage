from services.rpc_services.rpc_requests import RequestRpc

covid_db_api = RequestRpc(
    url='http://covid-db-api.default/',
    username='covid_db_api',
    password='FoolishPassword',
    token_url='http://covid-db-api.default/token/'
)
