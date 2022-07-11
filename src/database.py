import logging
import os
import psycopg2


class Database:
    """
    A database of paths.
    """

    def __init__(
        self,
        user="convertium",
        password="convertium",
        host="postgres",
        port=5432,
        dbname="convertium",
    ):
        logging.debug("Initializing database")

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname

        if "CONVERTIUM_DB_USER" in os.environ:
            self.user = os.environ["CONVERTIUM_DB_USER"]

        if "CONVERTIUM_DB_PASSWORD" in os.environ:
            self.password = os.environ["CONVERTIUM_DB_PASSWORD"]

        if "CONVERTIUM_DB_HOST" in os.environ:
            self.host = os.environ["CONVERTIUM_DB_HOST"]

        if "CONVERTIUM_DB_PORT" in os.environ:
            self.port = os.environ["CONVERTIUM_DB_PORT"]

        if "CONVERTIUM_DB_DNNAME" in os.environ:
            self.dbname = os.environ["CONVERTIUM_DB_DNNAME"]

        with psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.dbname,
        ) as conn:
            with conn.cursor() as curr:
                try:
                    curr.execute(
                        "CREATE TABLE IF NOT EXISTS paths (path TEXT PRIMARY KEY);"
                    )
                    logging.debug("Database initialized")
                except Exception as e:  # pragma: no cover
                    logging.exception("Could not create database {}".format(e))
                    exit(1)

    def contains(self, path: str) -> bool:
        logging.debug("Checking if %s is in database", path)
        with psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.dbname,
        ) as conn:
            with conn.cursor() as curr:
                try:
                    curr.execute("SELECT * FROM paths WHERE path = %s;", (path,))
                    return curr.rowcount > 0
                except Exception:
                    logging.exception("Could not check if %s is in database", path)
                    return True

    def add(self, path: str) -> None:
        logging.debug("Adding %s to database", path)
        with psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.dbname,
        ) as conn:
            with conn.cursor() as curr:
                try:
                    curr.execute("INSERT INTO paths (path) VALUES (%s);", (path,))
                except Exception:  # pragma: no cover
                    logging.exception("Could not add %s to database", path)
