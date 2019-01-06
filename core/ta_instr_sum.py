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

sys.path.append(os.path.abspath(sett.get_path_core() ))
from get_instr_perf_summ import *
from sa_numeric import *

import pymysql.cursors
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

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
                        self.tp_1_s = row[4] #lower 95 first row row[4]
                    if (i == 8):
                        self.ent_2_b = row[2] #lower 80 last row row[2]
                        self.sl_2_b = row[4] #lower 95 last row row [4]
                        self.tp_2_b = row[5] #upper 95 last row row[5]
                        self.ent_2_s = row[3] #upper 80 last row row[3]
                        self.sl_2_s = row[5] #upper 95 last row row[5]
                        self.tp_2_s = row[4] #lower 95 last row row[4]
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

def get_forecast_pct(lp,fp):
    try:
        lpf = float(lp)
        fpf = float(fp)
        p = (fpf - lpf)/lpf
    except:
        p = 0
    return p

def update_forecast_table(s,wf,frc,d,pip):
    try:

        cr_d = connection.cursor(pymysql.cursors.SSCursor)
        sql_d = "SELECT unit FROM instruments WHERE symbol = '"+s+"'"
        cr_d.execute(sql_d)
        rs_d = cr_d.fetchall()
        for row in rs_d:
            unit = row[0]

        w_forecast_display_info = str(round(float(wf*100),2)) + " " + unit
        if unit == 'pips':
            w_forecast_display_info = str(round(float(wf*10000),0)) +" "+ unit
        if unit == '%':
            w_forecast_display_info = str(round(float(wf*100),2)) + unit



        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "UPDATE instruments SET w_forecast_change='"+str(wf)+"', w_forecast_display_info='"+ w_forecast_display_info +"' WHERE symbol='"+s+"'"
        cr.execute(sql)
        connection.commit()

        sql = "UPDATE price_instruments_data SET target_price = "+str(frc)+" WHERE (date>="+ d +" AND symbol='"+s+"' AND target_price =0) "
        cr.execute(sql)
        connection.commit()
        print(sql)
    except Exception as e: print(e)

def update_instruments_table(s,y1_pct,m6_pct,m3_pct,m1_pct,w1_pct,wf_pct,
trade_entry_buy_1,trade_tp_buy_1,trade_sl_buy_1,
trade_entry_buy_2,trade_tp_buy_2,trade_sl_buy_2,
trade_entry_sell_1,trade_tp_sell_1,trade_sl_sell_1,
trade_entry_sell_2,trade_tp_sell_2,trade_sl_sell_2):
    try:

        cr_d = connection.cursor(pymysql.cursors.SSCursor)
        sql_d = "SELECT decimal_places FROM instruments WHERE symbol='"+s+"' "
        cr_d.execute(sql_d)
        rs_d = cr_d.fetchall()
        for row in rs_d:
            decimal_places = row[0]

        sql_d = "SELECT price_close, date FROM price_instruments_data WHERE symbol='"+ s +"' ORDER BY date DESC LIMIT 1 "
        cr_d.execute(sql_d)
        rs_d = cr_d.fetchall()
        for row in rs_d:
            last_price = row[0]
            last_date = row[1]


        y1_pct = round(float(y1_pct), 3)
        m6_pct = round(float(m6_pct), 3)
        m3_pct = round(float(m3_pct), 3)
        m1_pct = round(float(m1_pct), 3)
        w1_pct = round(float(w1_pct), 3)
        wf_pct = round(float(wf_pct), 3)

        if wf_pct >=0:
            signal_type = "buy"
            signal_dir = '<'
        else:
            signal_type = "sell"
            signal_dir = '<'

        signal_entry = signal_dir + str( round( float(last_price), decimal_places ) )
        d = last_date + timedelta(days=7)
        signal_expiration = d.strftime("%Y%m%d")


        trade_entry_buy_1 = round(float(trade_entry_buy_1), decimal_places); trade_tp_buy_1 = round(float(trade_tp_buy_1), decimal_places); trade_sl_buy_1 = round(float(trade_sl_buy_1), decimal_places)
        trade_entry_buy_2 = round(float(trade_entry_buy_2), decimal_places); trade_tp_buy_2 = round(float(trade_tp_buy_2), decimal_places); trade_sl_buy_2 = round(float(trade_sl_buy_2), decimal_places)
        trade_entry_sell_1 = round(float(trade_entry_sell_1), decimal_places); trade_tp_sell_1 = round(float(trade_tp_sell_1), decimal_places); trade_sl_sell_1 = round(float(trade_sl_sell_1), decimal_places)
        trade_entry_sell_2 = round(float(trade_entry_sell_2), decimal_places); trade_tp_sell_2 = round(float(trade_tp_sell_2), decimal_places); trade_sl_sell_2 = round(float(trade_sl_sell_2), decimal_places)

        if trade_entry_buy_1 < 0 or trade_entry_buy_2 < 0 or trade_entry_sell_1 < 0 or trade_entry_sell_2 < 0:
            trade_entry_buy_1 = round( last_price, decimal_places ); trade_entry_buy_2 = round( last_price, decimal_places )
            trade_entry_sell_1 = round( last_price, decimal_places ); trade_entry_sell_2 = round( last_price, decimal_places )

        if trade_tp_buy_1 < 0:
            trade_tp_buy_1 = 0
        if trade_sl_buy_1 < 0:
            trade_sl_buy_1 = 0
        if trade_tp_buy_2 < 0:
            trade_tp_buy_2 = 0
        if trade_sl_buy_2 < 0:
            trade_sl_buy_2 = 0
        if trade_tp_sell_1 < 0:
            trade_tp_sell_1 = 0
        if trade_sl_sell_1 < 0:
            trade_sl_sell_1 = 0
        if trade_tp_sell_2 < 0:
            trade_tp_sell_2 = 0
        if trade_sl_sell_2 < 0:
            trade_sl_sell_2 = 0

        sql = "SELECT price_close FROM price_instruments_data WHERE symbol='"+ str(s) +"' ORDER BY date LIMIT 30"
        stdev_st = get_stdev(sql)
        maximum_dd_st = get_mdd(sql)
        romad_st = get_romad(sql)

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "UPDATE instruments SET y1="+str(y1_pct)+",m6="+str(m6_pct)+",m3="+str(m3_pct)+",m1="+str(m1_pct)+",w1="+str(w1_pct)+",wf="+str(wf_pct)+","+\
        "signal_type='"+ signal_type +"',signal_entry='"+ signal_entry +"',signal_expiration="+ str(signal_expiration) + ","+\
        "trade_1_entry="+str(trade_entry_buy_1)+",trade_1_tp="+str(trade_tp_buy_1)+",trade_1_sl="+str(trade_sl_buy_1)+",trade_1_type='buy',"+\
        "trade_2_entry="+str(trade_entry_buy_2)+",trade_2_tp="+str(trade_tp_buy_2)+",trade_2_sl="+str(trade_sl_buy_2)+",trade_2_type='buy',"+\
        "trade_3_entry="+str(trade_entry_sell_1)+",trade_3_tp="+str(trade_tp_sell_1)+",trade_3_sl="+str(trade_sl_sell_1)+",trade_3_type='sell',"+\
        "trade_4_entry="+str(trade_entry_sell_2)+",trade_4_tp="+str(trade_tp_sell_2)+",trade_4_sl="+str(trade_sl_sell_2)+",trade_4_type='sell', "+\
        "stdev_st="+ str(stdev_st)+", maximum_dd_st="+ str(maximum_dd_st)+","+   +"  "+\
        "WHERE symbol='"+s+"' "
        print(sql_i)
        cr_i.execute(sql_i)
        connection.commit()

    except Exception as e: print(e)


def get_instr_sum(s,uid,asset_class,dn,pip):

    m = 1
    #Convert from percentage to pips for forex
    if asset_class == 'FX:':
        m = 10000

    instr_data = instr_sum_data(s,uid)
    forc_data = forecast_data(uid)
    # ---
    y1_pct = float(instr_data.get_pct_1Yp() )* m
    m6_pct = float(instr_data.get_pct_6Mp() )* m
    m3_pct = float(instr_data.get_pct_3Mp() )* m
    m1_pct = float(instr_data.get_pct_1Mp() )* m
    w1_pct = float(instr_data.get_pct_1Wp() )* m
    frc_pt = forc_data.get_frc_pt()
    lp_pt = instr_data.get_lp()
    wf = get_forecast_pct(lp_pt, frc_pt )
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
        update_forecast_table(s,wf,frc_pt,dn,pip)
        update_instruments_table(s,y1_pct,m6_pct,m3_pct,m1_pct,w1_pct,wf_pct,
        trade_entry_buy_1,trade_tp_buy_1,trade_sl_buy_1,
        trade_entry_buy_2,trade_tp_buy_2,trade_sl_buy_2,
        trade_entry_sell_1,trade_tp_sell_1,trade_sl_sell_1,
        trade_entry_sell_2,trade_tp_sell_2,trade_sl_sell_2)

    except Exception as e: print(e)
