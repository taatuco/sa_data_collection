# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
from datetime import timedelta
import time
import csv
import random

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def set_portf_symbol():
    r = ''
    try:
        symbol = ''
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT part_three FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = symbol + row[0]
        d = datetime.datetime.now(); frmd = datetime.datetime.strftime(d, '%d')
        symbol = symbol + frmd
        r = get_portf_suffix() + symbol.upper()
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def set_portf_fullname(s,ac,m,st):
    #portf: symbol, asset_class_name, market_label, strategy_type
    r = ''
    try:
        fullname = s.replace(get_portf_suffix(),'')
        r = fullname + ' ' + m + ' ' + ac + ' ' + st
    except Exception as e: print(e)
    return r

def get_portf_description(ac,m,st):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portf_description FROM labels WHERE lang = '"+ get_lang() +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: portf_description = row[0]
        nickname = get_nickname()
        market_asset_class = ac + ' ' + m + ' '+ st
        portf_description = portf_description.replace('{market_asset_class}',market_asset_class)
        portf_description = portf_description.replace('{nickname}',nickname)
        r = portf_description
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_strategy():
    try:
        pass
    except Exception as e: print(e)

def gen_portf():
    try:

        #Scan Asset Class and create portfolio if not reach threshold
        pass


    except Exception as e: print(e)
