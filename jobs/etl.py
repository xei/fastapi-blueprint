"""
This ETL script is responsible for extracting data from
an operational database, transform it to features and
load it into the feature store (Redis instance here).
"""

from datetime import datetime, timedelta
import os
import sys

import pyodbc
import redis


ODBC_DRIVER: str = 'ODBC Driver 17 for SQL Server'
DB_HOST: str = os.getenv('DB_HOST', 'sql-server')
DB_PORT: str = os.getenv('DB_PORT', '1433')
DB_NAME: str = os.getenv('DB_NAME', 'database')
DB_USER: str = os.getenv('DB_USER', 'root')
DB_PASS: str = os.getenv('DB_PASS', 'password')

REDIS_HOST: str = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASS: str = os.getenv('REDIS_PASS', 'password')
REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
REDIS_KEY_PREFIX = 'blueprint'

DAYS_OFFSET = 1


db_connection_string: str = (f'DRIVER={{{ODBC_DRIVER}}};'
                             f'SERVER={DB_HOST},{DB_PORT};'
                             f'DATABASE={DB_NAME};'
                             f'UID={DB_USER};'
                             f'PWD={DB_PASS}')

try:
    connection = pyodbc.connect(db_connection_string)
except Exception as e:
    print(f"Database is not healthy!\n{str(e)}", file=sys.stderr)
    exit(1)


redis_client = redis.Redis(host=REDIS_HOST,
                           port=REDIS_PORT,
                           password=REDIS_PASS,
                           db=REDIS_DB)
try:
    redis_client.ping()
except Exception as e:
    print(f"Redis is not healthy!\n{str(e)}", file=sys.stderr)
    exit(1)


from_date: datetime = datetime.now() - timedelta(days=DAYS_OFFSET)

sql_query = (
        "SELECT    field1, field2"
        "FROM      Table1"
       f"WHERE     created_at >= '{from_date.strftime('%Y-%m-%d')}'"
)

cursor = connection.cursor()
try:
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Log the result for future investigation
    print(f"Results:\n{results}")

    redis_client.set(f"{REDIS_KEY_PREFIX}:tmp", results)
except Exception as e:
    print(str(e), file=sys.stderr)
finally:
    cursor.close()
    redis_client.close()


print(f"Job done at {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}, "
      f"for data from {from_date.strftime('%Y-%m-%d')} "
      f"to {datetime.now().strftime('%Y-%m-%d')}")