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
    
def count_users():
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "select count(uid) from users"
    cur.execute(sql,)
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def get_user_list(page):
    offset = (page - 1) * 10
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "select * from users where isDeleted=0 order by regDate desc, uid limit 10 offset %s"
    cur.execute(sql,(offset,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows