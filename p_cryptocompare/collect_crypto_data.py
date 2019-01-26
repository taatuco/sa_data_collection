# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import urllib.request
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
sql = "SELECT symbol_list.symbol, symbol_list.uid, symbol_list.fsym, symbol_list.tsym FROM symbol_list INNER JOIN instruments ON symbol_list.symbol = instruments.symbol WHERE instruments.asset_class = 'CR:'"
cr.execute(sql)
rs = cr.fetchall()
i = 1
for row in rs:
    s = row[0]
    uid = row[1]
    fsym = row[2]
    tsym = row[3]

    print(s+": "+ os.path.basename(__file__) )

    ### Cryptocompare API ######################################################
    url = "https://min-api.cryptocompare.com/data/histoday?fsym="+fsym+"&tsym="+tsym+"&limit=30&aggregate=1&e=CCCAGG"
    ############################################################################

    request = urllib.request.Request(url)
    opener = urllib.request.build_opener()
    response = opener.open(request)

    f = opener.open(request)
    j = json.loads(f.read())
    k = len(j['Data'])
    i= 1
    cr_i = connection.cursor(pymysql.cursors.SSCursor)
    while i<k:
        pc = j['Data'][i]['close']
        d = j['Data'][i]['time']
        dt = datetime.utcfromtimestamp(int(d))
        sql_i = "INSERT INTO price_instruments_data(symbol, date, price_close) VALUES ('"+s+"','"+dt.strftime('%Y%m%d')+"','"+str(pc)+"')"
        print(sql_i)
        try:
            cr_i.execute(sql_i)
            connection.commit()
            cr_i.close()
        except:
            pass
        i +=1
    cr_i.close()
cr.close()
