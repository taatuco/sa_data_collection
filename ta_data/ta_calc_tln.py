# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import csv
import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
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

from datetime import datetime, timedelta

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

        with connection.cursor() as cr:
            sql = "SELECT symbol, date FROM price_instruments_data WHERE symbol='"+ self.s +"' ORDER BY date DESC LIMIT 1"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                self.ed = row["date"]
        self.sd = self.ed - timedelta(days=self.p)                
        self.md = self.ed - timedelta(days=self.p2)

    def get_sd(self):
        return self.sd

    def get_ed(self):
        return self.ed

    def get_md(self):
        return self.md

    def get_val_frm_d(self,d,get_what):
        #get from date
        v = 0
        with connection.cursor() as cr:
            dr = ""
            sl = ""
            if d == self.sd:
                dr = "' AND date>"+self.sd+" AND date<"+self.md
            if d == self.ed:
                dr = "' AND date>"+self.md+" AND date<"+self.ed
            if get_what == "l":
                sl = "SELECT MIN(price_close) AS p "
            if get_what == "h":
                sl = "SELECT MAX(price_close) AS p "

            sql = sl + "WHERE symbol='"+self.s + dr
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                v = row["p"]

        return v



class tln_data:

    sd = datetime.datetime(2000, 1, 1, 1, 1)
    ed = datetime.datetime(2000, 1, 1, 1, 1)
    md = datetime.datetime(2000, 1, 1, 1, 1)
    get_this = ""
    sdv = 0
    edv = 0
    mdv = 0
    p = 0

    def __init__(self, symbol_id, period, get_what):
        pts = trend_pts(symbol_id, period)
        self.sd = pts.get_sd()
        self.ed = pts.get_ed()
        self.md = pts.get_md()
        self.p = period
        self.get_this = get_what
        self.sdv = pts.get_val_frm_d(self.sd, self.get_this)
        self.edv = pts.get_val_frm_d(self.ed, self.get_this)
        self.mdv = pts.get_val_frm_d(self.md, self.get_this)

    def get_pts(self,d,x1v):
        x = 0
        if d != self.sd and d != self.ed:                          
            if self.sdv > self.edv:
                x = x1v + ( (self.edv - self.sdv)/self.p )
            else:
                x = x1v + ( (self.sdv - self.edv)/self.p )
        elif d == self.sd:
            x = self.sdv
        else:
            x = self.edv
                
        return x
