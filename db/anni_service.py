import json, hashlib, base64
from mysql.connector import pooling
with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **config)

def get_anniv_list(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "SELECT * FROM anniversary WHERE adate >= %s and adate <= %s order by adate"
    cur.execute(sql,params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def insert(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO anniversary VALUES (default, %s, %s, %s)"
    cur.execute(sql,params)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row