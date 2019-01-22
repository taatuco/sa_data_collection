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

sys.path.append(os.path.abspath( sett.get_path_core() ))
from ta_calc_ma import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_pct_from_date(d, sql_select, lp):
    pct = 0
    pp = 0
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = sql_select + "AND date <= '"+ str(d) +"' ORDER BY date DESC LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        pp = row[0]

    if pp != 0:
        pct = ( (lp - pp) / pp)
    return pct


class instr_sum_data:
    s = ""
    uid = ""
    sql_select = ""
    sql_select_signal = ""
    ld = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Yp = datetime.datetime(2000, 1, 1, 1, 1)
    d_6Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_3Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wf = datetime.datetime(2000, 1, 1, 1, 1)
    lp = 0
    lp_signal = 0

    def __init__(self,symbol,uid):
        try:
            self.s = symbol

            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT symbol from symbol_list WHERE uid=" + str(uid)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: symbol_is_portf = row[0]
            if symbol_is_portf.find( get_portf_suffix() ) > -1 :
                self.sql_select = "SELECT price_close, date FROM chart_data WHERE symbol='"+ self.s +"' "
            else:
                self.sql_select = "SELECT price_close, date FROM price_instruments_data WHERE symbol='"+ self.s + "' "
                self.sql_select_signal = "SELECT signal_price, date from chart_data WHERE symbol='"+ self.s +"' AND forecast = 0 "
                sql = self.sql_select_signal+" ORDER BY Date DESC LIMIT 1"
                cr.execute(sql)
                rs = cr.fetchall()
                for row in rs: self.lp_signal = row[0];


            sql = self.sql_select+" ORDER BY Date DESC LIMIT 1"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: self.lp = row[0]; self.ld = row[1]

            self.uid = uid
            self.d_1Yp = self.ld - ( timedelta(days=365) )
            self.d_6Mp = self.ld - ( timedelta(days=180) )
            self.d_3Mp = self.ld - ( timedelta(days=90) )
            self.d_1Mp = self.ld - ( timedelta(days=30) )
            self.d_1Wp = self.ld - ( timedelta(days=7) )
            self.d_1Wf = 0
        finally:
            cr.close()

    def get_uid(self):
        return self.uid

    def get_lp(self):
        return self.lp

    def get_ticker(self):
        return self.s

    def get_pct_1Yp(self):
        str_date = self.d_1Yp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_6Mp(self):
        str_date = self.d_6Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_3Mp(self):
        str_date = self.d_3Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Mp(self):
        str_date = self.d_1Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Wp(self):
        str_date = self.d_1Wp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.lp))

    def get_pct_1Yp_signal(self):
        str_date = self.d_1Yp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_6Mp_signal(self):
        str_date = self.d_6Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_3Mp_signal(self):
        str_date = self.d_3Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1Mp_signal(self):
        str_date = self.d_1Mp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1Wp_signal(self):
        str_date = self.d_1Wp.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))
