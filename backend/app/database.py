from contextlib import contextmanager

import pymysql
from pymysql.cursors import DictCursor

from .config import settings


def ensure_schema() -> None:
    connection = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW COLUMNS FROM articles LIKE 'hidden'")
            hidden_column = cursor.fetchone()
            if hidden_column is None:
                cursor.execute(
                    """
                    ALTER TABLE articles
                    ADD COLUMN hidden TINYINT(1) NOT NULL DEFAULT 0
                    """
                )
    finally:
        connection.close()


@contextmanager
def get_connection():
    connection = pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=False,
    )
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
