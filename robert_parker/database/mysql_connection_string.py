# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv('DB_DRIVER', '')
DB_HOST = os.getenv('DB_HOST', '')
DB_PORT = os.getenv('DB_PORT', '')
DB_USERNAME = os.getenv('DB_USERNAME', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_DATABASE = os.getenv('DB_DATABASE', '')


def mysql_connection_string() -> str:
    """Returns mysql connection string"""
    return "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        DB_USERNAME,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT,
        DB_DATABASE,
    )
