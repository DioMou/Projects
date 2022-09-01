import json
import sys
import logging
import redis
import pymysql
import re


DB_HOST = "database-mp6-instance-1.ct2conjworys.us-east-1.rds.amazonaws.com"#RDS终端节点
DB_USER = "admin"#RDS user name
DB_PASS = "Jowaq8421?"#RDS password
DB_NAME = "mp6"#MySQL database created, not the instance created in RDB
DB_TABLE = "heroTable"#MySQL table name
REDIS_URL = "redis://mp6elc.erqbye.ng.0001.use1.cache.amazonaws.com:6379"#redis主终端节点


TTL = 10

class DB:
    def __init__(self, **params):
        params.setdefault("charset", "utf8mb4")
        params.setdefault("cursorclass", pymysql.cursors.DictCursor)

        self.mysql = pymysql.connect(**params)

    def query(self, sql):
        with self.mysql.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def get_idx(self, table_name):
        with self.mysql.cursor() as cursor:
            cursor.execute(f"SELECT MAX(id) as id FROM {table_name}")
            idx = str(cursor.fetchone()['id'] + 1)
            return idx

    def insert(self, idx, data):
        with self.mysql.cursor() as cursor:
            hero = data["hero"]
            power = data["power"]
            name = data["name"]
            xp = data["xp"]
            color = data["color"]
            
            sql = f"INSERT INTO heroTable (`id`, `hero`, `power`, `name`, `xp`, `color`) VALUES ('{idx}', '{hero}', '{power}', '{name}', '{xp}', '{color}')"

            cursor.execute(sql)
            self.mysql.commit()

def read(use_cache, indices, Database, Cache):
    read_result=[]
    for idx in indices:
        sql=f"SELECT * FROM heroTable where id={idx}"
        if use_cache:
            row=Cache.get(idx)
            if row:
                read_result.append(json.loads(row))
            else:
                data=Database.query(sql)[0]
                hero = data["hero"]
                power = data["power"]
                name = data["name"]
                xp = data["xp"]
                color = data["color"]
                temp=[str(idx),hero,power,name,str(xp),color]
                space=' '
                temp=space.join(temp)
                Cache.setex(idx, TTL,json.dumps(data))
                read_result.append(data)
        else:
            r=Database.query(sql)
            read_result.append(r)
            
    return read_result
    
    
def write(use_cache, sqls, Database, Cache):
    for sql in sqls:
        idx=Database.get_idx(DB_TABLE)
        if use_cache:
            hero = sql["hero"]
            power = sql["power"]
            name = sql["name"]
            xp = sql["xp"]
            color = sql["color"]
            print('hey',' ',idx)
            
            exist=Cache.get(idx)#redis.exists(idx)
            print('hey1')
            if not exist:#if not Cache.get(idx)
                Database.insert(idx,sql)
                Cache.setex(idx,TTL,json.dumps(sql))
            else:
                update_cmd = f"UPDATE heroTable SET hero=`hero`,power=`power`,name=`name`,xp=`xp`,color=`color` WHERE id={str(idx)}"
                record=Database.query(update_cmd)[0]
                Cache.setex(idx,TTL,str(record))
            # write through strategy
        else:
            Database.insert(idx,sql)



def lambda_handler(event, context):
    
    USE_CACHE = (event['USE_CACHE'] == "True")
    REQUEST = event['REQUEST']
    
    # initialize database and cache
    try:
        Database = DB(host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME)
    except pymysql.MySQLError as e:
        print("ERROR: Unexpected error: Could not connect to MySQL instance.")
        print(e)
        sys.exit()
        
    Cache = redis.Redis.from_url(REDIS_URL)
    
    result = []
    if REQUEST == "read":
        # event["SQLS"] should be a list of integers
        result = read(USE_CACHE, event["SQLS"], Database, Cache)
    elif REQUEST == "write":
        # event["SQLS"] should be a list of jsons
        write(USE_CACHE, event["SQLS"], Database, Cache)
        result = "write success"
    
    
    return {
        'statusCode': 200,
        'body': result
    }