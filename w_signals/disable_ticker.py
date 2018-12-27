# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
from pathlib import Path

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def disable_non_valid_ticker(s):
    try:
        d = datetime.datetime.now() - timedelta(days=10)
        d = d.strftime("%Y%m%d")

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT price_close FROM price_instruments_data WHERE symbol = '"+ s +"' AND date>"+ d +" "
        cr.execute(sql)
        rs = cr.fetchall()
        price_close = 0
        for row in rs:
            price_close = int(row[0])

        if price_close == 0:
            sql = "UPDATE symbol_list SET disabled=1 WHERE symbol='"+ s +"' "
            cr.execute(sql)
            connection.commit()

    except Exception as e: print(e)
