import sqlite3
import random
import database.queries as queries
import database.enums as enums

conn = sqlite3.connect("database/database.db")
for i in range(100):
    queries.add_athlete(
        conn=conn,
        firstname="John",
        lastname="Smith",
        gender=random.choice(["Male","Female","Not Specified"]),
        dob = "2000-12-25",
        maindiscipline=random.choice(enums.DISCIPLINES),
        patrolgroupid=random.randint(1,16),
        phone="0400000000",
        email="something@gmail.com",
        active=True
    )
conn.close()