import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('cma-artworks.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


def table_info(c, conn):
    rows1 = c.execute("SELECT * from artwork__department").fetchall()
    rows2 = c.execute("SELECT * from artwork").fetchall()
    rows3 = c.execute("SELECT * from creator").fetchall()
    rows4 = c.execute("SELECT * from department").fetchall()
    rows5 = c.execute("SELECT * from artwork__creator").fetchall()
    jsonss = {
        'artwork__department': json.dumps([dict(ix) for ix in rows1]),
        'artwork': json.dumps([dict(ix) for ix in rows2]),
        'creator': json.dumps([dict(ix) for ix in rows3]),
        'department': json.dumps([dict(ix) for ix in rows4]),
        'artwork__creator': json.dumps([dict(ix) for ix in rows5])
    }
    print(jsonss)
    conn.commit()
    conn.close()

    with open('artworks.txt', 'w') as f:
        f.write(str(jsonss))



table_info(c, conn)