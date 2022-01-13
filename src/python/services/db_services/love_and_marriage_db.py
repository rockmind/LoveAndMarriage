import logging
import sys
from pandas import DataFrame

from python.services.db_services.db_services import DBServices

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger(__name__)


class LoveAndMarriageDB:
    _db: DBServices = DBServices(host='192.168.0.80:5432', db_name='love_and_marriage',
                                 user='postgres', password='testpassword')

    @classmethod
    async def get_cases(cls, date_from=None, date_to=None) -> DataFrame:

        conditions = await cls._get_conditions(date_from, date_to)

        query = f"""
            SELECT day, sum(cases.cases) as cases, sum(deaths) as deaths, sum(recovered) as recovered
            FROM cases{conditions}
            GROUP BY day
            ORDER BY day DESC
        """
        logger.info(query)
        df = await cls._db.run_sql_query(query)
        return df

    @classmethod
    async def _get_conditions(cls, date_from, date_to):
        if date_to and date_from:
            conditions = f" WHERE day >= '{date_from}' AND day <= '{date_to}'"
        elif date_to:
            conditions = f" WHERE day <= '{date_to}'"
        elif date_from:
            conditions = f" WHERE day >= '{date_from}'"
        else:
            conditions = ''
        return conditions

    @classmethod
    async def get_provinces(cls, date_from=None, date_to=None) -> DataFrame:
        conditions = await cls._get_conditions(date_from, date_to)

        query = f'''
            SELECT
                day,
                id_province,
                sum(cases) as cases,
                sum(deaths) as deaths,
                sum(recovered) as recovered
            FROM cases{conditions}
            GROUP BY day, id_province
        '''
        df = await cls._db.run_sql_query(query)
        return df

