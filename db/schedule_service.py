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
def get_sched_list(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "SELECT * FROM schedule WHERE uid=%s and sdate >= %s and sdate <= %s"
    cur.execute(sql,params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
def delete(sid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "delete from schedule where sid= %s"
    cur.execute(sql,(sid,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row
def get_end_time():
    pass
def get_is_important():
    pass
def get_memo():
    pass
def insert(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO schedule VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql,params)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row
def update(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "update board set title=%s, s_date=%s, start_date_time=%s, end_date_time=%s, place=%s, memo=%s, is_important=%s where sid=%s and uid=%s"
    cur.execute(sql,params)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row