import json, hashlib, base64
from mysql.connector import pooling

with open('./mysql.json') as f:
    config_str = f.read()
config = json.loads(config_str)
pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **config)

UID_NOT_EXIST = 0
CORRECT_LOGIN = 1
WRONG_PASSWORD = 2

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

def login(uid,pwd):
    user = get_user(uid)
    pwd_sha256 = hashlib.sha256(pwd.encode())
    hashed_pwd = base64.b64encode(pwd_sha256.digest()).decode('utf-8')
    if user == None:
        return UID_NOT_EXIST
    elif hashed_pwd == user[1]:
        return CORRECT_LOGIN
    else:
        return WRONG_PASSWORD