import pandas as pd
import sqlalchemy
import src.config as config


class CovidDbService:
    db = sqlalchemy.create_engine(
        config.DATABASE_ENGINE,
    )

    def get_cases(self, from_date=None, to_date=None, country=None, provinces=None, districts=None):
        query = """
        SELECT *
        FROM cases
        WHERE day = '2021-10-03'
        """
        df_data = pd.read_sql('district', self.db)
        return df_data.to_dict()

