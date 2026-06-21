import sqlite3

conn = sqlite3.connect("db/nifty100.db")

rows = conn.execute("""
SELECT id
FROM companies
ORDER BY id
""").fetchall()

for row in rows:
    print(row[0])

conn.close()