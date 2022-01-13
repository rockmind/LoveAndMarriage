from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor

from sqlalchemy import create_engine
from pandas import read_sql, DataFrame


class DBServices:
    def __init__(self, host, db_name, user, password):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.password = password

        self._db_engine = create_engine(
            f'postgresql://{self.user}:{self.password}@{self.host}/{self.db_name}',
        )

    async def run_sql_query(self, query: str) -> DataFrame:
        with ThreadPoolExecutor() as pool:
            result = await get_running_loop().run_in_executor(pool, lambda: read_sql(query, self._db_engine))

        return result

    async def new_configuration(self, config):
        pass
