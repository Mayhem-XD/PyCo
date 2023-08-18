import json, hashlib, base64
from mysql.connector import pooling

with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **config)

def get_reply_list(bid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "SELECT r.rid, r.`comment`, r.regTime, r.isMine, r.uid, r.bid, u.uname \
        FROM reply AS r JOIN users AS u ON r.uid=u.uid WHERE bid=%s"
    cur.execute(sql,(bid,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def insert_reply(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO reply VALUES (default, %s, default, %s, %s, %s)"
    cur.execute(sql,params)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row

def delete_reply(rid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "delete from reply where rid=%s"
    cur.execute(sql,(rid,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row