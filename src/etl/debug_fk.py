import sqlite3

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT DISTINCT company_id
FROM profitandloss
WHERE company_id NOT IN
(
    SELECT id
    FROM companies
)
"""

rows = conn.execute(query).fetchall()

for row in rows:
    print(row[0])

conn.close()