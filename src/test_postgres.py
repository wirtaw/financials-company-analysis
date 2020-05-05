#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Module for test postgresql connection."""

# import the connect library from psycopg2
from psycopg2 import connect

TABLE_NAME = "some_table"

# declare connection instance
conn = connect(
    dbname="some_db",
    user="objectrocket",
    host="172.28.1.4",
    password="1234"
)

# declare a cursor object from the connection
cursor = conn.cursor()

# execute an SQL statement using the psycopg2 cursor object
cursor.execute(f"SELECT * FROM {TABLE_NAME};")

# enumerate() over the PostgreSQL records
for i, record in enumerate(cursor):
    print("\n", type(record))
    print(record)

# close the cursor object to avoid memory leaks
cursor.close()

# close the connection as well
conn.close()
