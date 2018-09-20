# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import datetime
from datetime import timedelta
import csv
import sys
import os
import os.path
import gc
import time

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

class trend_pts:

    sd = datetime.datetime(2000, 1, 1, 1, 1)
    ed = datetime.datetime(2000, 1, 1, 1, 1)
    md = datetime.datetime(2000, 1, 1, 1, 1)
    s = ""
    p = 0
    p2 = 0

    def __init__(self, s, p):
        self.s = s;
        self.p = p;
        self.p2 = p/2;

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT date FROM price_instruments_data "+\
                "WHERE symbol='"+ self.s +\
                "' ORDER BY date DESC LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        ttr = cr.rowcount

        for row in rs:
            self.ed = row[0]
        cr.close()
        self.sd = self.ed - timedelta(days=self.p)
        self.md = self.ed - timedelta(days=self.p2)

    def get_sd(self):
        return self.sd

    def get_ed(self):
        return self.ed

    def get_md(self):
        return self.md

    def get_val_frm_d(self,d,get_what):
        '''
        +LT bias: Positive/negative
        +ST bias: Positive/negative
        +RSI momentum: Weak, Neutral, Strong
        _____________________________________________
        +RSI average
        +200d moving average
        +50d moving average
        '''
        v = 0
        cr = connection.cursor(pymysql.cursors.SSCursor)
        dr = ""
        sl = ""
        if d == self.sd:
            dr = "' AND date>'"+str(self.sd)+"' AND date<'"+str(self.md)+"'"
        if d == self.ed:
            dr = "' AND date>'"+str(self.md)+"' AND date<'"+str(self.ed)+"'"
        if get_what == "l":
            sl = "SELECT MIN(price_close) AS p "
        if get_what == "h":
            sl = "SELECT MAX(price_close) AS p "

        sql = sl + "FROM price_instruments_data WHERE symbol='"+self.s + dr
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            v = row[0]
        cr.close()
        return v

class tln_data:

    sd = datetime.datetime(2000, 1, 1, 1, 1)
    ed = datetime.datetime(2000, 1, 1, 1, 1)
    md = datetime.datetime(2000, 1, 1, 1, 1)
    get_this = ""
    sdv = 0
    edv = 0
    p = 0
    s = ""

    def __init__(self, symbol, period, get_what):
        pts = trend_pts(symbol, period)
        self.s = symbol
        self.sd = pts.get_sd()
        self.ed = pts.get_ed()
        self.md = pts.get_md()
        self.p = period
        self.get_this = get_what
        self.sdv = pts.get_val_frm_d(self.sd, self.get_this)
        self.edv = pts.get_val_frm_d(self.ed, self.get_this)

    def get_slope(self):
        slp = 0
        try:
            slp =  (self.edv - self.sdv)/self.p
        except:
            pass
        return slp

    def get_sd(self):
        return self.sd

    def get_ed(self):
        return self.ed

def get_trend_line_data(s,uid):

    dw = datetime.datetime.today().weekday()

    tl_180_l = tln_data(s,180,"l")
    tl_180_h = tln_data(s,180,"h")
    tl_360_l = tln_data(s,360,"l")
    tl_360_h = tln_data(s,360,"h")
    t180_l_x1v = 0
    t180_h_x1v = 0
    t360_l_x1v = 0
    t360_h_x1v = 0
    sd = tl_360_l.get_sd()
    f = sett.get_path_ta_data_src()+"\\"+str(uid)+"t.csv"
    if not os.path.isfile(f) or dw == 6:
        try:
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT date, price_close "+\
                    "FROM price_instruments_data "+\
                    "WHERE symbol='"+ s +"' AND date>='"+ str(sd) +"'"+\
                    " ORDER BY date"
            cr.execute(sql)
            rs = cr.fetchall()
            ttr = cr.rowcount

            with open(f, 'w', newline='') as csvfile:
                fieldnames = ["180_sd", "180_slope","360_sd","360_slope"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                t180_sd = tl_180_l.get_sd()
                t180_slp = tl_180_l.get_slope()
                t360_sd = tl_360_l.get_sd()
                t360_slp = tl_360_l.get_slope()
                print(s +": "+ os.path.basename(__file__) )
                writer.writerow({"180_sd": str(t180_sd), "180_slope": t180_slp, "360_sd": str(t360_sd), "360_slope": t360_slp})
            cr.close()

        finally:
            del t180_sd
            del t180_slp
            del t360_sd
            del t360_slp
            gc.collect()
