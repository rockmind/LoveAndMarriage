import uvicorn
import logging
from os import getenv
from jsonrpcserver import Result, Success, method, Error
from pandas import read_json as pd_read_json
from services.base_app import get_base_rpc_app
from services import json_dumps
from covid_db_service import CovidDbService


app = get_base_rpc_app()


@method
async def set_cases(cases_df) -> Result:
    try:
        await CovidDbService.set_cases(pd_read_json(cases_df, convert_dates=['day']))
    except Exception as err:
        return Error(err)
    return Success({'Status': 'OK', 'Message': 'Data updated'})


@method
async def get_district_geojson(country=None) -> Result:
    try:
        data = await CovidDbService.get_district_geojson(country)
    except Exception as err:
        return Error(err)
    return Success(json_dumps(data))


@method
async def get_provinces_geojson(country=None) -> Result:
    logging.info('TEST')
    try:
        data = await CovidDbService.get_provinces_geojson(country)
    except Exception as err:
        return Error(err)
    return Success(json_dumps(data))


@method
async def get_district_cases(date_from=None, date_to=None) -> Result:
    try:
        df = await CovidDbService.get_district_cases(date_from, date_to)
    except Exception as err:
        return Error(err)
    return Success(df.to_json())


@method
async def get_provinces_cases(date_from=None, date_to=None) -> Result:
    try:
        df = await CovidDbService.get_provinces_cases(date_from, date_to)
    except Exception as err:
        return Error(err, message=f'{str(err)}')
    return Success(df.to_json())


@method
async def get_provinces_ids() -> Result:
    try:
        df = await CovidDbService.get_provinces_ids()
    except Exception as err:
        return Error(err)
    return Success(df.to_json())


@method
async def get_districts_ids() -> Result:
    try:
        df = await CovidDbService.get_districts_ids()
    except Exception as err:
        return Error(err)
    return Success(df.to_json())


if __name__ == "__main__":
    port = int(getenv('APP_PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port)
