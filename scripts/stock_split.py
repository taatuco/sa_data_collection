# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import time
import datetime
from datetime import timedelta

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()



def correct_stock_split_price(symbol,to_this_date_included, split_factor):
    try:

        import pymysql.cursors
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT date, price_close, target_price, ma200, ma10, ma20, ma30, ma40, ma50 FROM price_instruments_data WHERE symbol = "'+ symbol +'" AND date <= '+ str(to_this_date_included) +' '
        cr.execute(sql)
        rs = cr.fetchall()
        i = 1
        sql_update = ''
        for row in rs:
            this_date = row[0]
            price_close = row[1]
            target_price = row[2]
            ma200 = row[3]
            ma10 = row[4]
            ma20 = row[5]
            ma30 = row[6]
            ma40 = row[7]
            ma50 = row[8]
            new_price_close = price_close * split_factor
            new_target_price = target_price * split_factor
            new_ma200 = ma200 * split_factor
            new_ma10 = ma10 * split_factor
            new_ma20 = ma20 * split_factor
            new_ma30 = ma30 * split_factor
            new_ma40 = ma40 * split_factor
            new_ma50 = ma50 * split_factor
            sql_update = 'UPDATE price_instruments_data SET price_close = ' + str(new_price_close) + ', target_price = ' + str(new_target_price) +\
            ', ma200 = ' + str(new_ma200) + ', ma10 = ' + str(new_ma10) + ', ma20 = ' + str(new_ma20) + ', ma30 = ' + str(new_ma30) + ', ma40 = ' + str(new_ma40) + ', ma50 = ' + str(new_ma50) + ' ' +\
            'WHERE symbol = "'+ symbol +'" AND date = ' + str(this_date)

        cr.close()
        connection.close()

    except Exception as e: print(e)
