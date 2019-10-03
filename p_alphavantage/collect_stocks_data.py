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
api_key = 'XWOJ8KDFY4TLNYF0'
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
dtsql_g = dtb.strftime('%Y%m%d')
dtjson_g = dtb.strftime('%Y-%m-%d')

for row in rs:
    s = row[0]
    uid = row[1]
    avs = row[2]

    print(s+": "+ os.path.basename(__file__) )
    try:
        data = { "function": "TIME_SERIES_DAILY",
        "symbol": avs,
        "datatype": "json",
        "apikey": api_key }
        response = requests.get(url, data)
        data = response.json()
        a = (data['Time Series (Daily)'][dtjson_a])
        b = (data['Time Series (Daily)'][dtjson_b])
        c = (data['Time Series (Daily)'][dtjson_c])
        d = (data['Time Series (Daily)'][dtjson_d])
        e = (data['Time Series (Daily)'][dtjson_e])
        f = (data['Time Series (Daily)'][dtjson_f])
        g = (data['Time Series (Daily)'][dtjson_g])

        print(a['4. close'] + " " + a['2. high'] + " " + a['5. volume'])
        pc_a = a['4. close']
        pc_b = b['4. close']
        pc_c = c['4. close']
        pc_d = d['4. close']
        pc_e = e['4. close']
        pc_f = f['4. close']
        pc_g = g['4. close']

    except Exception as e:
        print(e)
        pass

    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_a +"','"+str(pc_a)+"')"
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_b +"','"+str(pc_b)+"')"
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_c +"','"+str(pc_c)+"')"
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_d +"','"+str(pc_d)+"')"
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_e +"','"+str(pc_e)+"')"
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_f +"','"+str(pc_f)+"')"
    except: pass
    try:
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_g +"','"+str(pc_g)+"')"
    except: pass
    
    print(sql_i)
    try:
        #cr_i.execute(sql_i)
        #connection.commit()
        gc.collect()
    except:
        pass
    cr_i.close()
cr.close()
