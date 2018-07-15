# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

'''
(Daiviet) Will Remove this code as not useful as we have decided
to not update and import to database and read directly from csv which
is faster as we realise it.
'''

import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()
import pymysql.cursors

def set_zero_fib_trend(symbol_id):

    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        ### get price_instruments_data for the corresponding symbol_id
        # clear previous data to accommodate new one
        with connection.cursor() as cr:
            sql = "UPDATE price_instruments_data SET "+\
                              "mt_trend_high=0, mt_trend_low=0, "+\
                              "st_trend_high=0, st_trend_low=0, "+\
                              "fib_0=0, fib_23_6=0, fib_38_2=0, "+\
                              "fib_61_8=0, fib_76_4=0, fib_100=0 "+\
                              " WHERE symbol='"+symbol_id+"'"
            cr.execute(sql)
            connection.commit()
    finally:
        connection.close()
