import sqlite3
import pandas as pd
import json

connect = sqlite3.connect('cma-artworks.db')
connect.row_factory = sqlite3.Row
c = connect.cursor()


def table_info(c, connect):
    rows_1 = c.execute("SELECT * from artwork__department").fetchall()
    rows_2 = c.execute("SELECT * from artwork").fetchall()
    rows_3 = c.execute("SELECT * from creator").fetchall()
    rows_4 = c.execute("SELECT * from department").fetchall()
    rows_5 = c.execute("SELECT * from artwork__creator").fetchall()

    h1= json.dumps([dict(ix) for ix in rows_1])
    h2= json.dumps([dict(ix) for ix in rows_2])
    h3= json.dumps([dict(ix) for ix in rows_3])
    h4= json.dumps([dict(ix) for ix in rows_4])
    h5=json.dumps([dict(ix) for ix in rows_5])
    js = {
        'artwork__department': h1,
        'artwork': h2,
        'creator': h3,
        'department': h4,
        'artwork__creator': h5
    }

    print(js)
    connect.commit()
    connect.close()

    with open('artworks.txt', 'w') as p:
        p.write(str(js))



table_info(c,connect)