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

#   0 bid 1 uid 2 title 3 content 4 modTime
#   5 viewCount 6 replyCount 7 files 8 uname

def get_board_count(field, query):
    conn = pool.get_connection()
    cur = conn.cursor()
    sql = "select count(bid) from board where isDeleted=0 AND %s like %s"
    cur.execute(sql,(field,query))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row