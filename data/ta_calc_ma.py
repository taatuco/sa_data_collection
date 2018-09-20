# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

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

def calc_ma(symbol_id, date_id, ma_period):

    import pymysql.cursors
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        ma_period = str(ma_period)
        ma = 0
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT AVG(price_close) as ma FROM price_instruments_data "+\
        "WHERE symbol='"+symbol_id+"' AND date<"+date_id+" "+\
        "ORDER BY date DESC LIMIT "+ma_period
        cr.execute(sql)
        rs = cr.fetchall()
        if rs:
            for row in rs:
                ma = row[0]
        cr.close()
        return(ma)

    finally:
        connection.close()
