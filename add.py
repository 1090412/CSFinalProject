import sqlite3
import database.queries as queries
import database.enums as enums

conn = sqlite3.connect("database/database.db")
conn.commit()
conn.close()