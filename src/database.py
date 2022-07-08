import logging
import psycopg2


class Database:
    """
    A database of paths.
    """
    def __init__(self):
        logging.debug('Initializing database')
        with psycopg2.connect(user='convertium', password='convertium', host='postgres', port=5432, dbname='convertium') as conn:
            with conn.cursor() as curr:
                try:
                    curr.execute('CREATE TABLE IF NOT EXISTS paths (path TEXT PRIMARY KEY);')
                    logging.debug('Database initialized')
                except Exception as e:
                    logging.exception('Could not create database {}'.format(e))
                    exit(1)

    def contains(self, path: str) -> bool:
        logging.debug('Checking if %s is in database', path)
        with psycopg2.connect(user='convertium', password='convertium', host='postgres', port=5432, dbname='convertium') as conn:
            with conn.cursor() as curr:
                try:
                    curr.execute('SELECT * FROM paths WHERE path = %s;', (path,))
                    return curr.rowcount > 0
                except Exception:
                    logging.exception('Could not check if %s is in database', path)
                    return True

    def add(self, path: str) -> None:
        logging.debug('Adding %s to database', path)
        with psycopg2.connect(user='convertium', password='convertium', host='postgres', port=5432, dbname='convertium') as conn:
            with conn.cursor() as curr:
                try:
                    curr.execute('INSERT INTO paths (path) VALUES (%s);', (path,))
                except Exception:
                    logging.exception('Could not add %s to database', path)
