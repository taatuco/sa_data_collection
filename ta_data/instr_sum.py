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

'''
ticker
lastPrice
1Y
6M
3M
1M
1W
1Wf
'''
def get_pct_from_date(d, sql_select):
    pct = 0
    pp = 0
    lp = self.lp
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = sql_select + "AND date <= '"+ str(d) +"' ORDER BY date DESC LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        pp = row[0]

    # ((new - old)/ old ) * 100
    if pp != 0:
        pct = ( (lp - pp) / pp) * 100
    return pct


class instr_sum_data:

    pct_1Yp = 0
    pct_6Mp = 0
    pct_3Mp = 0
    pct_1Mp = 0
    pct_1Wp = 0
    pct_1Wf = 0
    s = ""
    sql_select = ""
    ld = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Yp = datetime.datetime(2000, 1, 1, 1, 1)
    d_6Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_3Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wf = datetime.datetime(2000, 1, 1, 1, 1)
    lp = 0
    p_1Yp = 0
    p_6Mp = 0
    p_3Mp = 0
    p_1Mp = 0
    p_1Wp = 0
    p_1Wf = 0

    def __init__(self,symbol):
        try:
            self.s = symbol
            self.sql_select = "SELECT price_close, date FROM price_instruments_data "+\
                                "WHERE symbol='"+ self.s + "' "
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = self.sql_select+" ORDER BY Date DESC LIMIT 1"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                self.lp = row[0]
                self.ld = row[1]
            self.d_1Yp = self.ld - ( timedelta(days=365) )
            self.d_6Mp = self.ld - ( timedelta(days=180) )
            self.d_3Mp = self.ld - ( timedelta(days=90) )
            self.d_1Mp = self.ld - ( timedelta(days=30) )
            self.d_1Wp = self.ld - ( timedelta(days=7) )
            self.d_1Wf = 0
        finally:
            cr.close()

    def get_ticker:
        return self.s

    def get_last_price:
        return str( format(self.lp, '.2f') )

    def get_pct_1Yp:
        str_date = self.d_1Yp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select)) + "%"

    def get_pct_6Mp:
        str_date = self.d_6Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select)) + "%"

    def get_pct_3Mp:
        str_date = self.d_3Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select)) + "%"

def get_instr_sum(s):
    instr_data = instr_sum_data(s)
