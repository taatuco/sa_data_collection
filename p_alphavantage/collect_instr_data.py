# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import requests
import alpha_vantage
import json
import sys
import os
import gc
import datetime
import time
from datetime import timedelta
import random

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
connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

cr = connection.cursor(pymysql.cursors.SSCursor)
sql = "SELECT symbol_list.symbol, symbol_list.uid, symbol_list.alphavantage FROM symbol_list INNER JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
"WHERE instruments.asset_class = 'EQ:' AND symbol_list.alphavantage NOT LIKE '' "
cr.execute(sql)
rs = cr.fetchall()
i = 1
### Alphavantage API ######################################################
api_key_1 = 'XWOJ8KDFY4TLNYF0'
api_key_2 = 'QD7YF5M1XAQYSNUA'
api_key_3 = 'SMOLNVP8JUAC2OZ7'
url = "https://www.alphavantage.co/query"
############################################################################
dta = datetime.datetime.now() - timedelta(days=1)
dtb = datetime.datetime.now() - timedelta(days=2)
dtc = datetime.datetime.now() - timedelta(days=3)
dtd = datetime.datetime.now() - timedelta(days=4)
dte = datetime.datetime.now() - timedelta(days=5)
dtf = datetime.datetime.now() - timedelta(days=6)
dtg = datetime.datetime.now() - timedelta(days=7)

dtsql_a = dta.strftime('%Y%m%d')
dtjson_a = dta.strftime('%Y-%m-%d')
dtsql_b = dtb.strftime('%Y%m%d')
dtjson_b = dtb.strftime('%Y-%m-%d')
dtsql_c = dtc.strftime('%Y%m%d')
dtjson_c = dtc.strftime('%Y-%m-%d')
dtsql_d = dtd.strftime('%Y%m%d')
dtjson_d = dtd.strftime('%Y-%m-%d')
dtsql_e = dte.strftime('%Y%m%d')
dtjson_e = dte.strftime('%Y-%m-%d')
dtsql_f = dtf.strftime('%Y%m%d')
dtjson_f = dtf.strftime('%Y-%m-%d')
dtsql_g = dtg.strftime('%Y%m%d')
dtjson_g = dtg.strftime('%Y-%m-%d')

for row in rs:
    s = row[0]
    uid = row[1]
    avs = row[2]

    key = random.randint(1,3)
    if key == 1: api_key = api_key_1
    if key == 2: api_key = api_key_2
    if key == 3: api_key = api_key_3
    print(api_key)

    print(s+": "+ os.path.basename(__file__) )
    data = { "function": "TIME_SERIES_DAILY",
    "symbol": avs,
    "datatype": "json",
    "apikey": api_key }
    response = requests.get(url, data)
    data = response.json()
    try:
        a = (data['Time Series (Daily)'][dtjson_a])
    except: pass
    try:
        b = (data['Time Series (Daily)'][dtjson_b])
    except: pass
    try:
        c = (data['Time Series (Daily)'][dtjson_c])
    except: pass
    try:
        d = (data['Time Series (Daily)'][dtjson_d])
    except: pass
    try:
        e = (data['Time Series (Daily)'][dtjson_e])
    except: pass
    try:
        f = (data['Time Series (Daily)'][dtjson_f])
    except: pass
    try:
        g = (data['Time Series (Daily)'][dtjson_g])
    except: pass

    try:
        pc_a = a['4. close']
    except: pass
    try:
        pc_b = b['4. close']
    except: pass
    try:
        pc_c = c['4. close']
    except: pass
    try:
        pc_d = d['4. close']
    except: pass
    try:
        pc_e = e['4. close']
    except: pass
    try:
        pc_f = f['4. close']
    except: pass
    try:
        pc_g = g['4. close']
    except: pass

    cr_i = connection.cursor(pymysql.cursors.SSCursor)

    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_a +"','"+str(pc_a)+"')"
        #cr_i.execute(sql_i)
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_b +"','"+str(pc_b)+"')"
        #cr_i.execute(sql_i)
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_c +"','"+str(pc_c)+"')"
        #cr_i.execute(sql_i)
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_d +"','"+str(pc_d)+"')"
        #cr_i.execute(sql_i)
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_e +"','"+str(pc_e)+"')"
        #cr_i.execute(sql_i)
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_f +"','"+str(pc_f)+"')"
        #cr_i.execute(sql_i)
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_g +"','"+str(pc_g)+"')"
        #cr_i.execute(sql_i)
    except: pass

    try:
        connection.commit()
        gc.collect()
    except:
        pass
    cr_i.close()
cr.close()
