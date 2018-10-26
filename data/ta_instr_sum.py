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
from pathlib import Path

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

class forecast_data:
    ent_1_b = 0
    sl_1_b = 0
    tp_1_b = 0
    ent_1_s = 0
    sl_1_s = 0
    tp_1_s = 0
    ent_2_b = 0
    sl_2_b = 0
    tp_2_b = 0
    ent_2_s = 0
    sl_2_s = 0
    tp_2_s = 0
    frc_pt = 0

    def __init__(self, uid):
        forc_src = sett.get_path_src()
        ext = ".csv"
        file_str = forc_src+str(uid)+'f.csv'
        filepath = Path(file_str)
        if filepath.exists():
            with open(file_str) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                i = 1
                for row in readCSV:
                    if (i == 2):
                        self.ent_1_b = row[2] #lower 80 first row row[2]
                        self.sl_1_b = row[4] #lower 95 first row row[4]
                        self.tp_1_b = row[5] #upper 95 first row row[5]
                        self.ent_1_s = row[3] #upper 80 first row row[3]
                        self.sl_1_s = row[5] #upper 95 first row row[5]
                        self.tp_1_s = row[3] #lower 95 first row row[3]
                    if (i == 8):
                        self.ent_2_b = row[2] #lower 80 last row row[2]
                        self.sl_2_b = row[4] #lower 95 last row row [4]
                        self.tp_2_b = row[5] #upper 95 last row row[5]
                        self.ent_2_s = row[3] #upper 80 last row row[3]
                        self.sl_2_s = row[5] #upper 95 last row row[5]
                        self.tp_2_s = row[3] #lower 95 last row row[3]
                        self.frc_pt = row[1] #forecast point 1W
                    i +=1
        print(str(uid) +": "+ os.path.basename(__file__) )


    def get_frc_pt(self):
        return self.frc_pt

    def get_entry_buy(self,p):
        if (p == 1):
            v = self.ent_1_b
        else:
            v = self.ent_2_b
        return v

    def get_sl_buy(self,p):
        if (p == 1):
            v = self.sl_1_b
        else:
            v = self.sl_2_b
        return v

    def get_tp_buy(self,p):
        if (p == 1):
            v = self.tp_1_b
        else:
            v = self.tp_2_b
        return v

    def get_entry_sell(self,p):
        if (p == 1):
            v = self.ent_1_s
        else:
            v = self.ent_2_s
        return v

    def get_sl_sell(self,p):
        if (p == 1):
            v = self.sl_1_s
        else:
            v = self.sl_2_s
        return v

    def get_tp_sell(self,p):
        if (p == 1):
            v = self.tp_1_s
        else:
            v = self.tp_2_s
        return v

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
    ld = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Yp = datetime.datetime(2000, 1, 1, 1, 1)
    d_6Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_3Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wf = datetime.datetime(2000, 1, 1, 1, 1)
    lp = 0

    def __init__(self,symbol,uid):
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

def get_forecast_pct(lp,fp):
    try:
        lpf = float(lp)
        fpf = float(fp)
        p = (fpf - lpf)/lpf
    except:
        p = 0
    return p

def update_forecast_table(s,wf):
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "UPDATE instruments SET w_forecast_change='"+str(wf)+"' WHERE symbol='"+s+"'"
        cr.execute(sql)
        connection.commit()
    except:
        pass

def get_instr_sum(s,uid,pip):

    #Convert to pips for FX instruments
    m = pip

    instr_data = instr_sum_data(s,uid)
    forc_data = forecast_data(uid)
    f = sett.get_path_src()+"\\"+str(uid)+"s.csv"
    # ---
    y1_pct = float(instr_data.get_pct_1Yp() )* m
    m6_pct = float(instr_data.get_pct_6Mp() )* m
    m3_pct = float(instr_data.get_pct_3Mp() )* m
    m1_pct = float(instr_data.get_pct_1Mp() )* m
    w1_pct = float(instr_data.get_pct_1Wp() )* m
    wf = get_forecast_pct(instr_data.get_lp(), forc_data.get_frc_pt() )
    wf_pct =  wf * m
    # --- (1)
    trade_entry_buy_1 = forc_data.get_entry_buy(1)
    trade_tp_buy_1 = forc_data.get_tp_buy(1)
    trade_sl_buy_1 = forc_data.get_sl_buy(1)
    # --- (2)
    trade_entry_buy_2 = forc_data.get_entry_buy(2)
    trade_tp_buy_2 = forc_data.get_tp_buy(2)
    trade_sl_buy_2 = forc_data.get_sl_buy(2)
    # --- (3)
    trade_entry_sell_1 = forc_data.get_entry_sell(1)
    trade_tp_sell_1 = forc_data.get_tp_sell(1)
    trade_sl_sell_1 = forc_data.get_sl_sell(1)
    # --- (4)
    trade_entry_sell_2 = forc_data.get_entry_sell(2)
    trade_tp_sell_2 = forc_data.get_tp_sell(2)
    trade_sl_sell_2 = forc_data.get_sl_sell(2)
    # ---
    try:
        update_forecast_table(s,wf)
        with open(f, mode="w", newline = "") as csvfile:
            fieldnames = ["y1", "m6", "m3", "m1", "w1","wf",
            "trade_1_entry", "trade_1_tp", "trade_1_sl", "trade_1_type",
            "trade_2_entry", "trade_2_tp", "trade_2_sl", "trade_2_type",
            "trade_3_entry", "trade_3_tp", "trade_3_sl", "trade_3_type",
            "trade_4_entry", "trade_4_tp", "trade_4_sl", "trade_4_type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({"y1": str(y1_pct), "m6": str(m6_pct), "m3": str(m3_pct), "m1": str(m1_pct), "w1": str(w1_pct), "wf": str(wf_pct),
            "trade_1_entry": str(trade_entry_buy_1), "trade_1_tp": str(trade_tp_buy_1), "trade_1_sl": str(trade_sl_buy_1), "trade_1_type": "buy",
            "trade_2_entry": str(trade_entry_buy_2), "trade_2_tp": str(trade_tp_buy_2), "trade_2_sl": str(trade_sl_buy_2), "trade_2_type": "buy",
            "trade_3_entry": str(trade_entry_sell_1), "trade_3_tp": str(trade_tp_sell_1), "trade_3_sl": str(trade_sl_sell_1), "trade_3_type": "sell",
            "trade_4_entry": str(trade_entry_sell_2), "trade_4_tp": str(trade_tp_sell_2), "trade_4_sl": str(trade_sl_sell_2), "trade_4_type": "sell"})
    except:
        pass
