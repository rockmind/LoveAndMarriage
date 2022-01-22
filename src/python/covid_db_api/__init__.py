import uvicorn
import logging
from os import getenv
from jsonrpcserver import Result, Success, method, Error
from pandas import read_json as pd_read_json
from services.base_app import get_base_rpc_app
from covid_db_service import CovidDbService

from services.log_config import config_logging
config_logging()

logger = logging.getLogger('CovidDbApi')

logger.info('Start app...')
app = get_base_rpc_app('CovidDbApi')
logger.info('App started!')

logger.info('Initialize CovidDB connection...')
covid_db = CovidDbService()
logger.info('CovidDB connection initialized!')


@method
async def set_cases(cases_df) -> Result:
    try:
        await CovidDbService.set_cases(pd_read_json(cases_df, convert_dates=['date']))
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success({'Status': 'OK', 'Message': 'Data updated'})


@method
async def set_geojson(geojson_df) -> Result:
    logger.info('Run set_geojson')
    try:
        await CovidDbService.set_geojson_data(pd_read_json(geojson_df))
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success({'Status': 'OK', 'Message': 'Data updated'})


@method
async def get_district_geojson(country=None) -> Result:
    try:
        data = await CovidDbService.get_district_geojson(country)
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success(data)


@method
async def get_provinces_geojson(country=None) -> Result:
    try:
        data = await CovidDbService.get_provinces_geojson(country)
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success(data)


@method
async def get_district_cases(date_from=None, date_to=None) -> Result:
    try:
        df = await CovidDbService.get_district_cases(date_from, date_to)
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success(df.to_json())


@method
async def get_provinces_cases(date_from=None, date_to=None) -> Result:
    try:
        df = await CovidDbService.get_provinces_cases(date_from, date_to)
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success(df.to_json())


@method
async def get_provinces_ids() -> Result:
    try:
        df = await CovidDbService.get_provinces_ids()
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success(df.to_json())


@method
async def get_districts_ids() -> Result:
    try:
        df = await CovidDbService.get_districts_ids()
    except Exception as err:
        return Error(code=503, message=f'Internal problem with services. Error details: {err}')
    return Success(df.to_json())


if __name__ == "__main__":
    port = int(getenv('APP_PORT', 8000))

    config = {}

    # this is default (site-packages\uvicorn\main.py)
    config['log_config'] = {
        'version': 1, 'disable_existing_loggers': True,
        'formatters': {'default': {'()': 'uvicorn.logging.DefaultFormatter', 'fmt': '|||%(levelprefix)s %(message)s',
                                   'use_colors': None},
                       'access': {'()': 'uvicorn.logging.AccessFormatter',
                                  'fmt': '|||%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'}},
        'handlers': {
            'default': {'formatter': 'default', 'class': 'logging.StreamHandler', 'stream': 'ext://sys.stderr'},
            'access': {'formatter': 'access', 'class': 'logging.StreamHandler', 'stream': 'ext://sys.stdout'}},
        'loggers': {'uvicorn': {'handlers': ['default'], 'level': 'INFO'},
                    'uvicorn.error': {'level': 'INFO', 'handlers': ['default'], 'propagate': False},
                    'uvicorn.access': {'handlers': ['access'], 'level': 'INFO', 'propagate': False},
                    },
    }

    uvicorn.run(app, host='0.0.0.0', port=port, **config)
