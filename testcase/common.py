# -*- coding: utf-8 -*-

# @File: common
# @Author : "Sampson"
# @Detail :
import redis
import platform
import os
import configparser
import pymysql


def conf_section(env, databaseType):
    if databaseType == "redis":
        confSection = "redis-%s" % env
        return confSection

    elif databaseType == "mysql":
        confSection = "db-mysql-%s" % env
        return confSection


def getConfig(env,databaseType):
    conf_path = '/config/myConfig' if platform.system() != 'Windows' else '\config\myConfig'
    conf_file_path = os.path.abspath(os.path.dirname(__file__)) + conf_path
    conf = configparser.RawConfigParser()
    conf.read(filenames=conf_file_path, encoding='utf-8')
    if databaseType == "redis":
        confSection = conf_section(env, databaseType)
        if confSection:
            host = conf.get(confSection, "host")
            port = conf.get(confSection, "port")
            password = conf.get(confSection, "password")
            return {"host": host, "port": port, "password": password}
        else:
            return
    elif databaseType == "mysql":
        confSection = conf_section(env, databaseType)
        if confSection:
            host = conf.get(confSection, "host")
            port = conf.get(confSection, "port")
            username = conf.get(confSection, "username")
            password = conf.get(confSection, "password")
            charset = conf.get(confSection, "charset")

            return {"host": host, "port": port, "username": username, "password": password, "charset": charset}
        else:
            return



def connectMysql(env, databaseType="mysql"):
    hostInfo = getConfig(env, databaseType)
    connect = pymysql.connect(
        host=hostInfo["host"],
        port=hostInfo["port"],
        user=hostInfo["username"],
        passwd=hostInfo["password"],
        charset=hostInfo["charset"],
        cursorclass=pymysql.cursors.DictCursor
    )
    connect = connect
    cursor = connect.cursor()
    return cursor




def connectRedis(env, databaseType="redis", db=0):
    hostInfo = getConfig(env, databaseType)
    print(hostInfo)
    pool = redis.ConnectionPool(host=hostInfo["host"], port=hostInfo["port"], db=db, password=hostInfo["password"])
    r = redis.Redis(connection_pool=pool)
    return r

def delRedis(r, channel, open_id, union_id, user_id):
    try:
        print(r.delete("login:user:session:1000001:%s:%s" % (channel, user_id)))
        print(r.delete("user:brandId:channel:appUserId:1000001:%s:%s" % (channel, open_id)))
        print(r.delete("user:brandId:channel:unionid:1000001:%s:%s" % (channel, union_id)))
        print(r.delete("tourist:brandId:channel:appUserId:1000001:%s:%s" % (channel, open_id)))
        print(r.delete("user:brandId:userId:1000001:%s:%s" % (channel, user_id)))

    except Exception as msg:
        print("出错啦：%s" % msg)

if __name__ == '__main__':

    """
    支付宝的 open_id 和 union_id 均为 user_oauth 表的 identifier 字段数据
    """
    run = "Z"

    if run == "W":
        env = "staging"
        channel = "W"
        db = 0
        open_id = "onsAE0S4WSrwHYwBUD-W1ncD1sJg"
        union_id = "oZ3J71dlZ7rLj2cJf94z_Q2EdJwc"
        user_id = "122957617"
    else:
        env = "staging"
        channel = "Z"
        db = 0
        open_id = "2088502813153020"
        union_id = "2088502813153020"
        user_id = "1100000089"



    r = connectRedis(env, db=db)
    delRet = delRedis(r, channel, open_id, union_id, user_id)
