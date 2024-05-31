'''File that creates a dashboard of data.'''
from os import environ

import pandas as pd
import altair as alt
import streamlit as st
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import execute_values, RealDictCursor, RealDictRow
from psycopg2.extensions import connection


def time_graph(data):

    return alt.Chart(data).mark_line().encode(
        alt.X("start_time", title='Time'),
        alt.Y("consumption", title='Consumption (kWh)')
    )


def get_db_connection() -> connection:
    """Returns a connection to the database."""

    return connect(
        dbname=environ["DB_NAME"],
        user=environ["DB_USER"],
        cursor_factory=RealDictCursor
    )


def all_consumption_data(conn_: connection) -> pd.DataFrame:
    """Returns a Dataframe of all data."""

    with conn_.cursor() as cur:
        cur.execute(f""" SELECT *
                    FROM consumption;""")
        data = cur.fetchall()

    return pd.DataFrame(data)


if __name__ == '__main__':
    load_dotenv()
    conn = get_db_connection()

    st.altair_chart(time_graph(all_consumption_data(conn)),
                    use_container_width=True)
