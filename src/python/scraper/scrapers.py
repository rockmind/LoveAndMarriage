from urllib.request import urlopen

import requests

from collections import OrderedDict
from pandas import concat as pd_concat, read_json as pd_read_json, read_csv as pd_read_csv, merge as pd_merge
from pandas import DataFrame, Timestamp
from datetime import datetime

from os import remove as os_remove
from zipfile import ZipFile

import config as config
from services.rpc_services import covid_db_api
from services import json_dumps, json_load


async def scrap_geojson():
    print('staa')

    with urlopen(config.PL_DISTRICTS_DIVISION_GEOJSON) as response:
        pl_districts = json_load(response)

    with urlopen(config.PL_PROVINCES_DIVISION_GEOJSON) as response:
        pl_provinces = json_load(response)

    df = DataFrame([
        {
            'id_cntry': 136,
            'provinces': json_dumps(pl_provinces),
            'districts': json_dumps(pl_districts)
        }
    ])

    await covid_db_api.rpc_request(OrderedDict(
        set_geojson={'geojson_df': df.to_json()}
    ))


async def scrap_actual_data():
    data_path = 'https://www.arcgis.com/sharing/rest/content/items/6ff45d6b5b224632a672e764e04e8394/data'

    raw_df = pd_read_csv(data_path, encoding='cp1250', sep=';')

    district_df, province_df = await _get_districts_and_provinces_ids()

    df = raw_df[raw_df['powiat_miasto'] != 'Cały kraj']
    df = pd_merge(df, province_df, how='left', left_on=['wojewodztwo'], right_on=['province_name'])
    df = pd_merge(df, district_df, how='left', left_on=['id_province', 'powiat_miasto'],
                  right_on=['id_province', 'district_name'])

    df['id_district'] = df['id_district'].astype('Int64')
    df['id_province'] = df['id_province'].astype('Int64')
    df['id_cntry'] = 136
    df.rename(inplace=True, columns={
        "stan_rekordu_na": "date",
        "liczba_przypadkow": "cases",
        "zgony": "deaths",
        "liczba_ozdrowiencow": "recovered"
    })
    df = df[['date', 'id_cntry', 'id_province', 'id_district', 'cases', 'deaths', 'recovered']]

    await covid_db_api.rpc_request(OrderedDict(
        set_cases={'cases_df': df.to_json()}
    ))


async def scrap_historical_data():

    df = pd_concat([df async for df in _get_historical_data()], ignore_index=True)

    await covid_db_api.rpc_request(OrderedDict(
        set_cases={'cases_df': df.to_json()}
    ))


async def _get_historical_data_old():
    data_path = config.PL_OLDEST_HISTORICAL_DATA
    raw_df = pd_read_csv(
        data_path, encoding='cp1250', sep=';',
        parse_dates=['Data'],
        dayfirst=True,
        thousands=' ',
    )
    raw_df.rename(inplace=True, columns={
        "Data": "date",
        "Nowe przypadki": config.CASES,
        "Zgony": config.DEATHS,
        "Ozdrowieńcy (dzienna)": config.RECOVERED
    })
    raw_df['id_cntry'] = 136
    raw_df['id_province'] = 16
    df = raw_df[['date', 'id_cntry', 'id_province', 'cases', 'deaths', 'recovered']]
    return df


async def _get_historical_data():
    df_old = await _get_historical_data_old()
    yield df_old

    data_path = config.PL_HISTORICAL_DATA
    district_df, province_df = await _get_districts_and_provinces_ids()

    def parse_data(file_name, zip_file):
        try:
            with zip_file.open(file_name) as my_file:
                parse_raw_df = pd_read_csv(my_file, encoding='cp1250', sep=';')
        except UnicodeDecodeError:
            with zip_file.open(file_name) as my_file:
                parse_raw_df = pd_read_csv(my_file, encoding='utf8', sep=';')
        return parse_raw_df

    # %%
    get_response = requests.get(data_path, stream=True)
    zipfilename = 'data_files.zip'
    with open(zipfilename, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    maps = {}
    with ZipFile(zipfilename) as zip_file:
        files = zip_file.namelist()
        files.remove('readme.txt')

        for filename in files:

            raw_df = parse_data(filename, zip_file)
            df = raw_df[raw_df['powiat_miasto'] != 'Cały kraj']

            df = pd_merge(df, province_df, how='left', left_on=['wojewodztwo'], right_on=['province_name'])
            df = pd_merge(df, district_df, how='left', left_on=['id_province', 'powiat_miasto'],
                          right_on=['id_province', 'district_name'])

            df['id_district'] = df['id_district'].astype('Int64')
            df['id_province'] = df['id_province'].astype('Int64')
            df['id_cntry'] = 136
            df['date'] = Timestamp(datetime.strptime(filename[:8], '%Y%m%d').strftime('%Y-%m-%d'))
            if 'liczba_ozdrowiencow' not in df.columns:
                df['liczba_ozdrowiencow'] = None
            df.rename(inplace=True, columns={
                "liczba_przypadkow": "cases",
                "zgony": "deaths",
                "liczba_ozdrowiencow": "recovered"
            })
            df = df[['date', 'id_cntry', 'id_province', 'id_district', 'cases', 'deaths', 'recovered']]
            maps[filename] = len(df.index)
            yield df

    os_remove(zipfilename)


async def _get_districts_and_provinces_ids():
    try:
        districts_ids = await covid_db_api.rpc_request('get_districts_ids')
        provinces_ids = await covid_db_api.rpc_request("get_provinces_ids")
    except Exception as err:
        raise Exception(f'Could not get provinces and districts ids. Err: {err}')
    district_df = pd_read_json(districts_ids['result'])
    province_df = pd_read_json(provinces_ids['result'])
    return district_df, province_df
