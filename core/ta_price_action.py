# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
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
import pymysql.cursors


db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def count_day(w,date_start,date_end):
    r = 0
    try:
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        if w == 'u': sql = 'SELECT COUNT(*) FROM price_instruments_data WHERE change_1d >0 AND date >=' + str(date_start) + ' AND date <=' + str(date_end)
        if w == 'd': sql = 'SELECT COUNT(*) FROM price_instruments_data WHERE change_1d <0 AND date >=' + str(date_start) + ' AND date <=' + str(date_end)
        if w == 'avgu': sql = 'SELECT AVG(change_1d) FROM price_instruments_data WHERE change_1d >0 AND date >=' + str(date_start) + ' AND date <=' + str(date_end)
        if w == 'avgd': sql = 'SELECT AVG(change_1d) FROM price_instruments_data WHERE change_1d <0 AND date >=' + str(date_start) + ' AND date <=' + str(date_end)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_price_action_score(symbol_id, date_start, date_end):
    r = 0
    try:
        #1. count number of days up in num_period
        day_up = count_day('u',date_start,date_end)
        #2. count number of days down in num_period
        day_down = count_day('d',date_start,date_end)
        #3. average volatility percentage of days up in num_period
        day_avg_vol_up = count_day('avgu',date_start,date_end)
        #4. average volatility percentage of days down in num_period
        day_avg_vol_down = count_day('avgd',date_start,date_end)
        # a = days_up / days_down
        a = day_up / day_down
        # b = vol_days_up / vol_days_down
        b = day_avg_vol_up / day_avg_vol_down
        # (a + b) / 2
        index = (a + b) / 2
    except Exception as e: print(e)
    return r
