import uvicorn

from jsonrpcserver import Result, Success, method, Error
from os import getenv
from services.base_app.base_app import get_base_rpc_app
from scraper.scrapers import scrap_historical_data as historical_data_scrap
from scraper.scrapers import scrap_actual_data as actual_data_scrap
from scraper.scrapers import scrap_geojson


app = get_base_rpc_app()


@method
async def scrap_geojson_data() -> Result:

    try:
        await scrap_geojson()
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success({'Status': 'OK', 'Message': 'Geojson data updated'})


@method
async def scrap_historical_data() -> Result:

    try:
        await historical_data_scrap()
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success({'Status': 'OK', 'Message': 'Covid cases data updated'})


@method
async def scrap_actual_data() -> Result:

    try:
        await actual_data_scrap()
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success({'Status': 'OK', 'Message': 'Covid cases data updated'})


if __name__ == "__main__":
    port = int(getenv('APP_PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port, log_level='info')
