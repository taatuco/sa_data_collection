# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()
    
def calc_ma(symbol_index, date_index, ma_period):

    #define database username and password and other variable regarding access to db
    db_usr = access_obj.username()
    db_pwd = access_obj.password()
    db_name = access_obj.db_name()
    db_srv = access_obj.db_server()

    # Use PyMySQL to access MySQL database
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
        with connection.cursor() as cursor:
            sql = "SELECT AVG(price_close) as ma FROM price_instruments_data "+\
            "WHERE symbol='"+symbol_index+"' AND date<"+date_index+" "+\
            "ORDER BY date DESC LIMIT "+ma_period
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                for row in result:
                    ma = row["ma"]
            return(ma)

    finally:
        connection.close()
