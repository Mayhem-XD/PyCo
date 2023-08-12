import json
from mysql.connector import pooling

with open('../mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **config)

def get_user(uid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "select * from users where uid=%s"
    cur.execute(sql,(uid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row
    