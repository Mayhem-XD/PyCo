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

def register_user(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "insert into users values (%s, %s, %s, %s, default, default, %s, %s)"
    cur.execute(sql,params)
    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

def update_user(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "update users set uname=%s, pwd=%s, email=%s, profile=%s, addr=%s where uid=%s"
    cur.execute(sql,params)
    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

def delete_user(uid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "update users set isDeleted=1 uid=%s"
    cur.execute(sql,(uid,))
    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()