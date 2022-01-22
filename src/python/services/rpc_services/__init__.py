from services.rpc_services.rpc_requests import RequestRpc

covid_db_api = RequestRpc(
    url='http://covid-db-api.love-and-marriage/',
    username='covid_db_api',
    password='FoolishPassword',
    token_url='http://covid-db-api.love-and-marriage/token/'
)
