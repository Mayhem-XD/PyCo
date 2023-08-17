import json, hashlib, base64
from mysql.connector import pooling

with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **config)

def get_board(bid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "SELECT b.bid, b.uid, b.title, b.content, b.modTime, b.viewCount, b.replyCount, b.files, u.uname \
        FROM board AS b JOIN users AS u ON b.uid=u.uid WHERE b.bid=%s"
    cur.execute(sql,(bid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row
