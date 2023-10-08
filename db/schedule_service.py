import json, hashlib, base64
from mysql.connector import pooling
with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **config)

def get_schedule(sid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "select * from schedule where sid = %s"
    cur.execute(sql,(sid,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row
def get_place():
    pass
def get_start_time():
    pass
def get_end_time():
    pass
def get_is_important():
    pass
def get_memo():
    pass
def insert(params):
    pass