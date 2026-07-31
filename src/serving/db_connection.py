import os

from sqlalchemy import create_engine

from src.core.config_loader import ConfigLoader


class DBConnection:
    """
    Creates PostgreSQL database connection.
    """

    def __init__(self):

        config = ConfigLoader().get_config()

        postgres = config["postgres"]

        self.host = postgres["host"]
        self.port = postgres["port"]
        self.database = postgres["database"]
        self.username = postgres["username"]
        self.password = os.getenv(
            "POSTGRES_PASSWORD",
            postgres.get("password", "")
        )

    def get_engine(self):

        connection_string = (
            f"postgresql+psycopg2://"
            f"{self.username}:{self.password}"
            f"@{self.host}:{self.port}/"
            f"{self.database}"
        )

        engine = create_engine(connection_string)

        return engine