import os

from urllib.parse import quote_plus

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

        print("Host:", self.host)
        print("Port:", self.port)
        print("Database:", self.database)
        print("Username:", self.username)
        print("Password:", repr(self.password))

        connection_string = (
            f"postgresql+psycopg2://"
            f"{self.username}:{quote_plus(self.password)}"
            f"@{self.host}:{self.port}/"
            f"{self.database}"
        )

        print(connection_string)

        return create_engine(connection_string)