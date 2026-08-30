import sqlite3
import random
import database.queries as queries
import database.enums as enums

conn = sqlite3.connect("database/database.db")
queries.add_supervisor(
    conn=conn,
    firstname="Gary",
    lastname="Gary",
    phone="0400000000",
    email="something@icloud.com"
)
for i in range(10):
    queries.add_patrolgroup(
        conn=conn,
        name=f"{i}th Patrol Group",
        supervisorid=1
    )
conn.close()