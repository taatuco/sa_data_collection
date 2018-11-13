# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
from datetime import timedelta
import csv
from pathlib import Path

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

import pymysql.cursors
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_forecast_pnl(s,uid):

    b = datetime.datetime.now() - timedelta(days=367)
    b_str = b.strftime("%Y%m%d")
    wdb = 7
    td = datetime.datetime.now()

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT price_close, target_price FROM price_instruments_data WHERE symbol ='"+s+"' AND date = "+ b_str
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        price_close = row[0]
        target_price = row[1]
