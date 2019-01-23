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
import time

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

import pymysql.cursors
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

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
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
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
        connection.close()
        self.sd = self.ed - timedelta(days=self.p)
        self.md = self.ed - timedelta(days=self.p2)

    def get_sd(self):
        return self.sd

    def get_ed(self):
        return self.ed

    def get_md(self):
        return self.md

    def get_val_frm_d(self,d,get_what):
        v = 0
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
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
        connection.close()
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

    def get_sdv(self):
        return self.sdv

    def get_edv(self):
        return self.edv

    def get_200ma_frm_d(self,d):
        v = 0
        s = self.s
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT ma200 FROM price_instruments_data WHERE (symbol ='"+s+"' AND date='"+str(d)+"') LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            v = row[0]
        cr.close()
        connection.close()
        return v

    def get_50ma_frm_d(self,d):
        v = 0
        s = self.s
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT AVG(price_close) AS p FROM price_instruments_data WHERE (symbol ='"+s+"' AND date<='"+str(d)+"') LIMIT 50"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            v = row[0]
        cr.close()
        connection.close()
        return v

    def get_rsi_avg(self,d,p):
        v = 0
        s = self.s
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT AVG(rsi14) AS rsi FROM price_instruments_data WHERE (symbol ='"+s+"' AND date<='"+str(d)+"') LIMIT " + str(p)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            v = row[0]
        cr.close()
        connection.close()
        return v

    def get_rsi_mom(self,v):
        try:
            if (v < 31):
                mm = "Oversold"
            if (v >30 and v <50):
                mm = "Weak"
            if (v >49 and v <70):
                mm = "Strong"
            if (v >69):
                mm = "Overbought"
        except:
            mm = ""
        return mm

def get_bias(sdv,edv):
    try:
        v = "Neutral"
        if (sdv > edv):
            v = "Negative"
        if (sdv < edv):
            v = "Positive"
    except:
        v = ""
    return v

def get_trend_line_data(s,uid):

    tl_180_l = tln_data(s,180,"l")
    tl_180_h = tln_data(s,180,"h")
    tl_360_l = tln_data(s,360,"l")
    tl_360_h = tln_data(s,360,"h")
    t180_l_x1v = 0
    t180_h_x1v = 0
    t360_l_x1v = 0
    t360_h_x1v = 0
    sd = tl_360_l.get_sd()
    f = sett.get_path_src()+"\\"+str(uid)+"t.csv"
    connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT date, price_close "+\
            "FROM price_instruments_data "+\
            "WHERE symbol='"+ s +"' AND date>='"+ str(sd) +"'"+\
            " ORDER BY date"
    cr.execute(sql)
    rs = cr.fetchall()
    ttr = cr.rowcount

    with open(f, 'w', newline='') as csvfile:
        fieldnames = ["180_sd", "180_slope_low","180_slope_high",
        "360_sd","360_slope_low","360_slope_high",
        "180_sdv_low","180_sdv_high","360_sdv_low","360_sdv_high",
        "st_lower_range","st_upper_range","lt_lower_range", "lt_upper_range",
        "st_rsi_avg", "lt_rsi_avg", "st_rsi_mom", "lt_rsi_mom",
        "ma200","ma50", "st_bias", "lt_bias"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        t180_sd = tl_180_l.get_sd()
        t180_ed = tl_180_l.get_ed()
        t360_ed = tl_360_l.get_ed()
        t180_slp_l = tl_180_l.get_slope()
        t180_slp_h = tl_180_h.get_slope()
        t360_sd = tl_360_l.get_sd()
        t360_slp_l = tl_360_l.get_slope()
        t360_slp_h = tl_360_h.get_slope()
        t180_sdv_l = tl_180_l.get_sdv()
        t180_sdv_h = tl_180_h.get_sdv()
        t360_sdv_l = tl_360_l.get_sdv()
        t360_sdv_h = tl_360_h.get_sdv()
        st_lower_range = tl_180_l.get_edv()
        st_upper_range = tl_180_h.get_edv()
        lt_lower_range = tl_360_l.get_edv()
        lt_upper_range = tl_360_h.get_edv()

        st_rsi_avg = tl_180_l.get_rsi_avg( t180_ed, 5)
        lt_rsi_avg = tl_360_l.get_rsi_avg( t360_ed, 50)

        st_rsi_mom = tl_180_l.get_rsi_mom(st_rsi_avg)
        lt_rsi_mom = tl_360_l.get_rsi_mom(lt_rsi_avg)
        ma_200_ed = tl_360_l.get_200ma_frm_d( t180_ed )
        ma_50_ed = tl_360_l.get_50ma_frm_d( t180_ed )
        ma_200_sd = tl_360_l.get_200ma_frm_d( t180_sd )
        ma_50_sd = tl_360_l.get_50ma_frm_d( t180_sd )
        st_bias = get_bias(ma_50_sd, ma_50_ed)
        lt_bias = get_bias(ma_200_sd, ma_200_ed)

        print(s +": "+ os.path.basename(__file__) )
        writer.writerow({"180_sd": str(t180_sd), "180_slope_low": str(t180_slp_l), "180_slope_high": str(t180_slp_h),
        "360_sd": str(t360_sd), "360_slope_low": str(t360_slp_l),"360_slope_high": str(t360_slp_h),
        "180_sdv_low": str(t180_sdv_l), "180_sdv_high": str(t180_sdv_h), "360_sdv_low": str(t360_sdv_l), "360_sdv_high": str(t360_sdv_h),
        "st_lower_range": str(st_lower_range), "st_upper_range": str(st_upper_range), "lt_lower_range": str(lt_lower_range), "lt_upper_range": str(lt_upper_range),
        "st_rsi_avg":str(st_rsi_avg), "lt_rsi_avg": str(lt_rsi_avg), "st_rsi_mom": str(st_rsi_mom), "lt_rsi_mom": str(lt_rsi_mom),
        "ma200": str(ma_200_ed), "ma50": str(ma_50_ed), "st_bias": str(st_bias), "lt_bias": str(lt_bias) })
    cr.close()
    connection.close()
