import logging
from typing import Dict

from pandas import DataFrame

from services.db_services.db_services import DBServices

logger = logging.getLogger(__name__)


class CovidDbService:
    _db: DBServices = DBServices(host='postgres.default:5432', db_name='covid',
                                 user='love_and_marriage', password='FoolishPassword')

    @classmethod
    async def set_cases(cls, cases_df: DataFrame):
        cases_df.to_sql('cases', cls._db.db_engine, if_exists='replace', index=False)

    @classmethod
    async def set_geojson_data(cls, df: DataFrame):
        df.to_sql('geojson', cls._db.db_engine, if_exists='replace', index=False)

    @classmethod
    async def get_provinces_geojson(cls, country=None) -> Dict:
        query = f"""
            SELECT provinces
            FROM geojson
            WHERE id_cntry=136
        """
        df = await cls._db.run_sql_query(query)
        return dict() if df.empty else df.provinces[0]

    @classmethod
    async def get_district_geojson(cls, country=None) -> Dict:
        query = f"""
                SELECT districts
                FROM geojson
                WHERE id_cntry=136
            """
        logger.info(query)
        df = await cls._db.run_sql_query(query)
        return dict() if df.empty else df.districts[0]

    @classmethod
    async def get_district_cases(cls, date_from=None, date_to=None, country='Polska') -> DataFrame:

        conditions = await cls._get_conditions(date_from, date_to)

        query = f"""
            SELECT date, sum(cases) as cases, sum(deaths) as deaths, sum(recovered) as recovered
            FROM cases
            {conditions}
            GROUP BY date
            ORDER BY date DESC
        """
        logger.info(query)
        df = await cls._db.run_sql_query(query)
        return df

    @classmethod
    async def get_provinces_cases(cls, date_from=None, date_to=None, country='Polska') -> DataFrame:
        conditions = await cls._get_conditions(date_from, date_to)

        query = f'''
            SELECT
                date,
                id_province,
                sum(cases) as cases,
                sum(deaths) as deaths,
                sum(recovered) as recovered
            FROM cases
            {conditions}
            GROUP BY date, id_province
        '''
        df = await cls._db.run_sql_query(query)
        return df

    @classmethod
    async def _get_conditions(cls, date_from, date_to):
        if date_to and date_from:
            conditions = f"WHERE date >= '{date_from}' AND date <= '{date_to}'"
        elif date_to:
            conditions = f"WHERE date <= '{date_to}'"
        elif date_from:
            conditions = f"WHERE date >= '{date_from}'"
        else:
            conditions = ''
        return conditions

    @classmethod
    async def get_countries(cls) -> DataFrame:
        query = f'''
            SELECT *
            FROM country
        '''
        df = await cls._db.run_sql_query(query)
        return df

    @classmethod
    async def get_districts_ids(cls) -> DataFrame:
        query = f'''
            SELECT *
            FROM district
        '''
        df = await cls._db.run_sql_query(query)
        return df

    @classmethod
    async def get_provinces_ids(cls) -> DataFrame:
        query = f'''
            SELECT *
            FROM province
        '''
        df = await cls._db.run_sql_query(query)
        return df
