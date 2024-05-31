'''A script that uploads data from consumption.csv into the database.'''
from os import environ

import pandas as pd
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import execute_values, RealDictCursor, RealDictRow
from psycopg2.extensions import connection


def extract_consumption():
    '''Extracts data from consumption.csv.'''
    data = pd.read_csv('consumption.csv')

    data[' Start'] = data[' Start'].astype(str)
    data['Time Difference'] = data[' Start'].apply(lambda x: x.strip()[-5:])
    data[' Start'] = data[' Start'].apply(lambda x: x.strip()[:-6])
    data[' End'] = data[' End'].astype(str).apply(lambda x: x.strip()[:-6])
    data[' Start'] = pd.to_datetime(data[' Start'], format='%Y-%m-%dT%H:%M:%S')
    data[' End'] = pd.to_datetime(data[' End'], format='%Y-%m-%dT%H:%M:%S')
    print(data.dtypes)
    return data


def get_db_connection() -> connection:
    """Returns a connection to the database."""

    return connect(
        dbname=environ["DB_NAME"],
        user=environ["DB_USER"],
        cursor_factory=RealDictCursor
    )


if __name__ == '__main__':
    data = extract_consumption().values.tolist()
    load_dotenv()
    conn = get_db_connection()

    with conn.cursor() as cur:
        cur.executemany("""INSERT INTO consumption (consumption,start_time,end_time, time_difference)
                    VALUES (%s,%s,%s, %s);""", (data))

    conn.commit()

    cur.close()
    conn.close()
