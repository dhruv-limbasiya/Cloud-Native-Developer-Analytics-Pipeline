from src.core.logger import Logger

from src.serving.db_connection import DBConnection


class PostgresWriter:
    """
    Writes DataFrame into PostgreSQL.
    """

    def __init__(self):

        self.logger = Logger.get_logger()

        self.engine = DBConnection().get_engine()

    def save(self, dataframe, table_name):

        dataframe.to_sql(
            name=table_name,
            con=self.engine,
            if_exists="replace",
            index=False,
        )

        self.logger.info(
            f"Loaded table -> {table_name}"
        )