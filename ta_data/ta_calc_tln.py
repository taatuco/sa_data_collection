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

from datetime import datetime, timedelta

class trend_pts:

    sd = datetime.datetime(2000, 1, 1, 1, 1)
    ed = datetime.datetime(2000, 1, 1, 1, 1)
    md = datetime.datetime(2000, 1, 1, 1, 1)
    x1 = datetime.datetime(2000, 1, 1, 1, 1) - timedelta(days=p)
    s = ""
    d = datetime.datetime(2000, 1, 1, 1, 1)
    p = 0

    def __init__(self, s, d, p):
        self.s = s;
        self.d = d;
        self.p = p;
        self.p2 = p/2;

        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cr:
            sql = "SELECT symbol, date FROM price_instruments_data WHERE symbol='"+ self.s +"' ORDER BY date DESC LIMIT 1"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                self.d = row["date"]
            self.ed = self.d

    def get_sd(self):
        self.sd = self.ed - timedelta(days=self.p)
        return self.sd

    def get_ed(self):
        return self.ed

    def get_md(self):
        self.md = self.ed - timedelta(days=self.p2)
        return self.md

    def get_x1(self):
        self.x1 = d - timedelta(days=1)
        return self.x1


class tln_data:

    sd = datetime.datetime(2000, 1, 1, 1, 1)
    ed = datetime.datetime(2000, 1, 1, 1, 1)
    md = datetime.datetime(2000, 1, 1, 1, 1)
    x1 = datetime.datetime(2000, 1, 1, 1, 1)
    get_this = ""

    def __init__(self, symbol_id, date_id, period, get_what):
        #period = 180 or 360
        pts = trend_pts(symbol_id, date_id, period)
        self.sd = pts.get_sd()
        self.ed = pts.get_ed()
        self.md = pts.get_md()
        self.x1 = pts.get_x1()
        #l for low, h for high
        self.get_this = get_what

    def get_t_l(self):
        sd = self.sd
        ed = self.ed
        md = self.md
        x1 = self.x1
        p = self.p
        x = 0

        #get the value

        if sdv > edv:
            x = x1v + ( (edv - sdv)/p )
            else
            x = x1v + ( (sdv - edv)/p )
        return x
