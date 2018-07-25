# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import datetime
from datetime import timedelta
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
            sql = "SELECT symbol, date FROM price_instruments_data "+\
                    "WHERE symbol='"+ self.s +\
                    "' ORDER BY date DESC LIMIT 1"
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
                v = row["p"]
        return v
    


class tln_data:

    sd = datetime.datetime(2000, 1, 1, 1, 1)
    ed = datetime.datetime(2000, 1, 1, 1, 1)
    md = datetime.datetime(2000, 1, 1, 1, 1)
    get_this = ""
    sdv = 0
    edv = 0
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

    def get_pts(self,d,x1v):
        x = 0
        try:
            if x1v == 0:
                x1v = self.sdv
            
            if d >= self.sd and d != self.ed:
                if self.sdv > self.edv:
                    x = x1v + ( (self.edv - self.sdv)/self.p )
                else:
                    x = x1v + ( (self.sdv - self.edv)/self.p )
            elif d == self.ed:
                x = self.edv
            else:
                x = 0
        except Exception as e: print(e)
        
        return x

def get_trend_line_data(s):

    tl_180_l = tln_data(s,180,"l")
    tl_180_h = tln_data(s,180,"h")
    tl_360_l = tln_data(s,360,"l")
    tl_360_h = tln_data(s,360,"h")
    dpts = trend_pts(s,360)
    t180_l_x1v = 0
    t180_h_x1v = 0    
    t360_l_x1v = 0
    t360_h_x1v = 0    
    sd = dpts.get_sd()
    f = "src\\"+ s +"_tl.csv"
       
    with connection.cursor() as cr:
        sql = "SELECT date, price_close "+\
                "FROM price_instruments_data "+\
                "WHERE symbol='"+ s +"' AND date>='"+ str(sd) +"'"+\
                " ORDER BY date"
        cr.execute(sql)
        rs = cr.fetchall()

        with open(f, 'w') as csvfile:
            fieldnames = ["date", "180_low","180_high","360_low","360_high"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in rs:
                d = row["date"]
                t180_l = tl_180_l.get_pts(d,t180_l_x1v)
                t180_h = tl_180_h.get_pts(d,t180_h_x1v)
                t180_l_x1v = t180_l
                t180_h_x1v = t180_h
                
                t360_l = tl_360_l.get_pts(d,t360_l_x1v)
                t360_h = tl_360_h.get_pts(d,t360_h_x1v)
                t360_l_x1v = t360_l
                t360_h_x1v = t360_h
                writer.writerow({"date": str(d), "180_low": t180_l, "180_high": t180_h, "360_low": t360_l, "360_high": t360_h})



            
