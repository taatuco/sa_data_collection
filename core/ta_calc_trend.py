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

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

class trend_data:

    ta_3d_trend = ''
    ta_5d_trend = ''
    ta_7d_trend = ''

    def __init__(self, symbol, datestr):
        try:

            ta_3d_count_up = 0 ; ta_3d_count_down = 0
            ta_5d_count_up = 0 ; ta_5d_count_down = 0
            ta_7d_count_up = 0 ; ta_7d_count_down = 0

            import pymysql.cursors
            connection = pymysql.connect(host=db_srv,
                                         user=db_usr,
                                         password=db_pwd,
                                         db=db_name,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT price_close FROM price_instruments_data "+\
            "WHERE symbol='"+ str(symbol) +"' AND date<="+ str(datestr) + " ORDER BY date LIMIT 7"
            cr.execute(sql)
            rs = cr.fetchall()
            i = 0
            previous_close = 0
            for row in rs:
                price_close = row[0]

                if i > 0:
                    if price_close > previous_close: ta_7d_count_up += 1
                    if price_close < previous_close: ta_7d_count_down += 1
                    if i >= 2:
                        if price_close > previous_close: ta_5d_count_up += 1
                        if price_close < previous_close: ta_5d_count_down += 1
                    if i >= 4:
                        if price_close > previous_close: ta_3d_count_up += 1
                        if price_close < previous_close: ta_3d_count_down += 1

                previous_close = price_close
                i += 1

            if ta_7d_count_up >= ta_7d_count_down:
                trend_data.ta_7d_trend = 'u'
            else:
                self.ta_7d_trend = 'd'

            if ta_5d_count_up >= ta_5d_count_down:
                trend_data.ta_5d_trend = 'u'
            else:
                trend_data.ta_5d_trend = 'd'

            if ta_3d_count_up >= ta_3d_count_down:
                trend_data.ta_3d_trend = 'u'
            else:
                trend_data.ta_3d_trend = 'd'


            cr.close()
            connection.close()


        except Exception as e: print( str(symbol_id) + " ::: " + str(e) )

    def get_3d_trend(self):
        return trend_data.ta_3d_trend

    def get_5d_trend(self):
        return trend_data.ta_5d_trend

    def get_7d_trend(self):
        return trend_data.ta_7d_trend
