# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import requests
import alpha_vantage
import json

import sys
import os
from datetime import datetime

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

for row in rs:
    s = row[0]
    uid = row[1]
    avs = row[2]

    print(s+": "+ os.path.basename(__file__) )

    data = { "function": "TIME_SERIES_DAILY",
    "symbol": avs,
    "interval" : "60min",
    "datatype": "json",
    "apikey": api_key }
    response = requests.get(url, data)
    data = response.json()
    a = (data['Time Series (Daily)'])
    keys = (a.keys())
    for key in keys:
        print(a[key] + " :: " + a[key]['4. close'] + " " + a[key]['2. high'] + " " + a[key]['5. volume'])


    #sql_i = "INSERT INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+dt.strftime('%Y%m%d')+"','"+str(pc)+"')"
    #print(sql_i)
    #try:
    #    cr_i.execute(sql_i)
    #    connection.commit()
    #    cr_i.close()
    #except:
    #    pass
    #cr_i.close()
cr.close()
