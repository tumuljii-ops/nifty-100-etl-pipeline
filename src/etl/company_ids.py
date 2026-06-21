import sqlite3

conn = sqlite3.connect("db/nifty100.db")

ids = [
    "ULTRACEMCO",
    "UNIONBANK",
    "UNITDSPR",
    "VBL",
    "VEDL",
    "WIPRO",
    "ZOMATO",
    "ZYDUSLIFE"
]

for company in ids:

    query = """
    SELECT COUNT(*)
    FROM companies
    WHERE id = ?
    """

    count = conn.execute(
        query,
        (company,)
    ).fetchone()[0]

    print(company, count)

conn.close()