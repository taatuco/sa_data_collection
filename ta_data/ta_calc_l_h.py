# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import datetime
import sys
import os
import time
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

import pymysql.cursors
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

def get_lh(what,symbol, date, period, count_row):
    try:
        lowest_price = 0
        highest_price = 0
        rv = 0

        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        if count_row == period:
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT MIN(price_close) as lowest, MAX(price_close) as highest FROM price_instruments_data "+\
                    "WHERE symbol='"+symbol+"' AND date<"+str(date)+" "+\
                    "LIMIT "+str(period)
            cr.execute(sql)
            r = cr.fetchall()
            for row in r:
                lowest_price = row[0]
                highest_price = row[1]
                time.sleep(0.2)
            cr.close()
        if what=="l":
            rv = lowest_price
        else:
            rv = highest_price

        return rv
    finally:
        connection.close()


# Notes:
# Retrieve Lowest or Highest point according to specified period

class low_high_data:

    r_c = 0
    s = ""
    p = 0
    d = datetime.datetime(2000, 1, 1, 1, 1)

    def __init__(self, symbol, date, period):
        try:
            connection = pymysql.connect(host=db_srv,
                                         user=db_usr,
                                         password=db_pwd,
                                         db=db_name,
                                         charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
            #with connection.cursor() as cr_c:
            cr_c = connection.cursor(pymysql.cursors.SSCursor)
            sql_c = "SELECT id FROM price_instruments_data "+\
                    "WHERE symbol='"+symbol+"' AND date<"+str(date)+" "+\
                    "LIMIT "+str(period)
            cr_c.execute(sql_c)
            r = cr_c.fetchall()
            self.r_c = cr_c.rowcount
            self.s = symbol
            self.d = date
            self.p = period
            cr_c.close()
        finally:
            connection.close()

    def get_low(self):
        rv = 0
        if self.r_c == self.p:
            rv = get_lh("l", self.s, self.d, self.p, self.r_c)
        return rv

    def get_high(self):
        rv = 0
        if self.r_c == self.p:
            rv = get_lh("h", self.s, self.d, self.p, self.r_c)
        return rv
