import sqlite3

conn = sqlite3.connect("../services/data_service/prices.db")
cursor = conn.cursor()

cursor.execute(("SELECT * FROM LatestPrice LIMIT 10"))
rows = cursor.fetchall()

print(rows)