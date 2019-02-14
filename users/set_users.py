# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
import time

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def set_user_uid():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=99))

def set_user_avatar_id():
    max = 19
    return random.randint(1,max)

def set_nickname():
    p1 = ''; p2 =''; num = ''
    r = ''
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT part_one FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: p1 = row[0]
        sql = "SELECT part_two FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: p2 = row[0]
        cr.close()
        num = str( get_random_num(99) )
        r = p1 + p2 + num
    except Exception as e: print(e)
    return r

def set_default_profile():
    r = ''
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT asset_class_id as p FROM asset_class UNION SELECT market_id as p FROM markets ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
        r = r.replace('PF:',''); r = r.replace('BD:','')
    except Exception as e: print(e)
    return r

def gen_users(n):
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        d = datetime.datetime.now() ; d = d.strftime('%Y%m%d')
        for i in range(n):
            if i == 0:
                default_user = 'smartalpha'
                uid = set_user_uid()
                name = default_user
                nickname = name
                username = name + '@smartalphatrade.com'
                password = set_user_uid()
                avatar_id  = set_user_avatar_id()
                created_on = str(d)
                default_profile = ''
                lang = 'en'
                is_bot = 1
            else:
                uid = set_user_uid()
                name = set_nickname()
                nickname = name
                username = name + '@' + nickname + '.com'
                password = set_user_uid()
                avatar_id  = set_user_avatar_id()
                created_on = str(d)
                default_profile = ''
                lang = 'en'
                is_bot = 1

            sql = "INSERT INTO users(uid, name, nickname, username, password, avatar_id, created_on, default_profile, lang, is_bot) VALUES "+\
            "('"+ str(uid) +"','"+ str(name) +"','"+ str(nickname) +"','"+ str(username) +"','"+ str(password) +"',"+ str(avatar_id) +",'"+ str(created_on) +"','"+ str(default_profile) +"','"+ str(lang) +"',"+str(is_bot)+")"
            print(sql)
            cr.execute(sql)
            connection.commit()
        cr.close()

    except Exception as e: print(e)

gen_users(2000)
