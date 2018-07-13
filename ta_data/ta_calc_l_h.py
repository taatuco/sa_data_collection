# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

# Notes:
# Retrieve Lowest or Highest point according to specified period


class low_high_data:

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
 
    def __init__(self, symbol_id, date_id, period):
        self.symbol = symbol_id
        self.date = date_id
        self.period = period

    def get_low(self):
        try:
            lowest_price = 0
            cr_c = connection.cursor(pymysql.cursors.SSCursor)
            sql_c = "SELECT id FROM price_instruments_data "+\
                    "WHERE symbol='"+self.symbol+"' AND date<"+str(self.date)+" "+\
                    "LIMIT "+self.period
            cr_c.execute(sql_l)
            r_c = cr_c.fetchall()
            
            if r_c.rowcount == self.period:
                cr_c.close()
                cr_l = connection.cursor(pymysql.cursors.SSCursor)
                sql_l = "SELECT MIN(price_close) as lowest, symbol, date FROM price_instruments_data "+\
                        "WHERE symbol='"+self.symbol+"' AND date<"+str(self.date)+" "+\
                        "LIMIT "+self.period
                cr_l.execute(sql_l)
                r_l = cr_l.fetchall()
                with row in cr_l:
                    lowest_price = row["lowest"]
            return lowest_price
        finally:
            cr_l.close()
        
    def get_high(self):
        pass


