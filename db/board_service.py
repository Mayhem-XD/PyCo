import json, hashlib, base64
from mysql.connector import pooling

with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **config)

LIST_PER_PAGE = 10;		# 한 페이지당 글 목록의 개수
PAGE_PER_SCREEN = 10;	# 한 화면에 표시되는 페이지 개수

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

def get_board_list(field, query, page):
    offset = (page - 1) * 10
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "SELECT b.bid, b.uid, b.title, b.modTime, b.viewCount, b.replyCount, u.uname FROM board AS b \
        JOIN users AS u ON b.uid=u.uid WHERE b.isDeleted=0 AND %s LIKE %s ORDER BY b.modTime DESC LIMIT 10 OFFSET %s"
    cur.execute(sql,(field,f'%{query}%', offset))
    row = cur.fetchall()
    cur.close()
    conn.close()
    return row

def get_board_count(field, query):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "select count(bid) from board where isDeleted=0 AND %s like %s"
    cur.execute(sql,(field,f'%{query}%'))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def insert_board(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "insert into board values(default, %s, %s, %s, default, default, default, default, %s)"
    cur.execute(sql,params)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row

def update_board(params):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "update board set title=%s, content=%s, modTime=now(), files=%s where bid=%s"
    cur.execute(sql,params)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row

def delete_board(bid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "UPDATE board SET isDeleted=1 WHERE bid=%s"
    cur.execute(sql,(bid,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row

def increase_count(field,bid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = f"UPDATE board SET {field}={field}+1 where bid = %s"
    cur.execute(sql,(bid,))
    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

def decrease_reply_count(bid):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "UPDATE board SET replyCount=replyCOunt-1 where bid = %s"
    cur.execute(sql,(bid,))
    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
