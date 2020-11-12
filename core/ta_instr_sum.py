""" Functionalities related to instruments data """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
from datetime import timedelta
import csv
from pathlib import Path
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_core()))
from get_instr_perf_summ import InstrumentSummaryData
from sa_numeric import get_stdev, get_mdd, get_romad, get_volatility_risk

sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


class ForecastData:
    """
    Get all related to forecast data such as target price, stop loss,
    price prediction...
    Args:
        Integer: Instrument Unique id
    """
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

    def __init__(self, uid, connection):

        target_price = -9
        date_today = datetime.datetime.now()
        date_today = date_today.strftime('%Y%m%d')
        date_yesterday = datetime.datetime.now() - timedelta(days=1)
        date_yesterday = date_yesterday.strftime('%Y%m%d')
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT price_instruments_data.target_price FROM trades "+\
        "JOIN symbol_list ON trades.symbol = symbol_list.symbol "+\
        "JOIN price_instruments_data ON "+\
        "(trades.symbol = price_instruments_data.symbol AND "+\
        "price_instruments_data.date = "+ str(date_yesterday) +") "+\
        "WHERE symbol_list.uid = "+ str(uid) +" AND trades.entry_date = " + str(date_today)
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            target_price = row[0]
        cursor.close()

        forc_src = SETT.get_path_src()
        file_str = forc_src+str(uid)+'f.csv'
        filepath = Path(file_str)
        if filepath.exists():
            with open(file_str) as csvfile:
                csv_file = csv.reader(csvfile, delimiter=',')
                i = 1
                for row in csv_file:
                    if i == 2:
                        self.ent_1_b = row[2] #lower 80 first row row[2]
                        self.sl_1_b = row[4] #lower 95 first row row[4]
                        self.tp_1_b = row[5] #upper 95 first row row[5]
                        self.ent_1_s = row[3] #upper 80 first row row[3]
                        self.sl_1_s = row[5] #upper 95 first row row[5]
                        self.tp_1_s = row[4] #lower 95 first row row[4]
                    if i == 8:
                        self.ent_2_b = row[2] #lower 80 last row row[2]
                        self.sl_2_b = row[4] #lower 95 last row row [4]
                        self.tp_2_b = row[5] #upper 95 last row row[5]
                        self.ent_2_s = row[3] #upper 80 last row row[3]
                        self.sl_2_s = row[5] #upper 95 last row row[5]
                        self.tp_2_s = row[4] #lower 95 last row row[4]
                        self.frc_pt = target_price
                    i += 1
        debug(str(uid) +": "+ os.path.basename(__file__))

    def get_frc_pt(self):
        """ Get forecast point """
        return self.frc_pt

    def get_entry_buy(self, pos):
        """ Get entry price for buy """
        if pos == 1:
            val = self.ent_1_b
        else:
            val = self.ent_2_b
        return val

    def get_sl_buy(self, pos):
        """ get stop loss for buy """
        if pos == 1:
            val = self.sl_1_b
        else:
            val = self.sl_2_b
        return val

    def get_tp_buy(self, pos):
        """ get target price for buy """
        if pos == 1:
            val = self.tp_1_b
        else:
            val = self.tp_2_b
        return val

    def get_entry_sell(self, pos):
        """ get entry price for sell """
        if pos == 1:
            val = self.ent_1_s
        else:
            val = self.ent_2_s
        return val

    def get_sl_sell(self, pos):
        """ get stop loss for sell """
        if pos == 1:
            val = self.sl_1_s
        else:
            val = self.sl_2_s
        return val

    def get_tp_sell(self, pos):
        """ get target price for sell """
        if pos == 1:
            val = self.tp_1_s
        else:
            val = self.tp_2_s
        return val

def get_forecast_pct(lprice, fprice):
    """
    Return the forecasted percentage price change
    Args:
        Double: Last price
        Double: Forecast price
    Returns:
        Double: Forecasted percentage change
    """
    if lprice != 0 and lprice is not None:
        lpf = float(lprice)
        fpf = float(fprice)
        result = (fpf - lpf)/lpf
    else:
        result = 0
    return result

def update_forecast_table(symbol, weekf, frc, date_this, connection):
    """
    Update forecast data table instruments and price_instruments_data
    Args:
        String: Instrument symbol
        Double: Week forecast change (if -999 it means the signal is cancelled)
        Double: Forecast weekly target price
        String: Date in string format YYYYMMDD
    Returns:
        None
    """

    cr_d = connection.cursor(pymysql.cursors.SSCursor)
    sql_d = "SELECT unit FROM instruments WHERE symbol = '"+symbol+"'"
    cr_d.execute(sql_d)
    rs_d = cr_d.fetchall()
    unit = ''
    for row in rs_d:
        unit = row[0]
    cr_d.close()
    w_forecast_display_info = ''
    if weekf != -999:
        w_forecast_display_info = str(round(float(weekf*100), 2)) + " " + unit
        if unit == 'pips':
            w_forecast_display_info = str(round(float(weekf*10000), 0)) +" "+ unit
        if unit == '%':
            w_forecast_display_info = str(round(float(weekf*100), 2)) + unit


    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "UPDATE instruments SET w_forecast_change='"+str(weekf)+"', w_forecast_display_info='"+\
    w_forecast_display_info +"' WHERE symbol='"+symbol+"'"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

    #cursor = connection.cursor(pymysql.cursors.SSCursor)
    #sql = "UPDATE price_instruments_data SET target_price = "+str(frc)+" WHERE (date>="+\
    #date_this +" AND symbol='"+symbol+"' AND target_price =0) "
    #debug(sql)
    #cursor.execute(sql)
    #connection.commit()
    #cursor.close()

def update_instruments_table(symbol, y1_pct, m6_pct, m3_pct, m1_pct, w1_pct, d1_pct, wf_pct,
                             trade_entry_buy_1, trade_tp_buy_1, trade_sl_buy_1,
                             trade_entry_buy_2, trade_tp_buy_2, trade_sl_buy_2,
                             trade_entry_sell_1, trade_tp_sell_1, trade_sl_sell_1,
                             trade_entry_sell_2, trade_tp_sell_2, trade_sl_sell_2,
                             y1_pct_signal, m6_pct_signal, m3_pct_signal,
                             m1_pct_signal, w1_pct_signal, sentiment, connection):
    """
    Update instrument table with summary data information
    Args:
        String: Instrument symbol
        Double: (24x) Various numerical data
    Returns:
        None
    """
    cr_d = connection.cursor(pymysql.cursors.SSCursor)
    sql_d = "SELECT decimal_places FROM instruments WHERE symbol='"+symbol+"' "
    cr_d.execute(sql_d)
    rs_d = cr_d.fetchall()
    decimal_places =  2
    for row in rs_d:
        decimal_places = row[0]
    cr_d.close()

    cr_d = connection.cursor(pymysql.cursors.SSCursor)
    sql_d = "SELECT price_close, date FROM price_instruments_data WHERE symbol='"+\
    symbol +"' ORDER BY date DESC LIMIT 1 "
    cr_d.execute(sql_d)
    rs_d = cr_d.fetchall()
    for row in rs_d:
        last_price = row[0]
        last_date = row[1]
    cr_d.close()

    y1_pct_signal = round(float(y1_pct_signal), 3)
    m6_pct_signal = round(float(m6_pct_signal), 3)
    m3_pct_signal = round(float(m3_pct_signal), 3)
    m1_pct_signal = round(float(m1_pct_signal), 3)
    w1_pct_signal = round(float(w1_pct_signal), 3)

    y1_pct = round(float(y1_pct), 3)
    m6_pct = round(float(m6_pct), 3)
    m3_pct = round(float(m3_pct), 3)
    m1_pct = round(float(m1_pct), 3)
    w1_pct = round(float(w1_pct), 3)
    d1_pct = round(float(d1_pct), 3)
    wf_pct = round(float(wf_pct), 3)

    date_last_month = datetime.datetime.now() - timedelta(days=30)
    date_last_month = date_last_month.strftime('%Y%m%d')
    sql = "SELECT price_close FROM price_instruments_data WHERE symbol='"+\
    str(symbol) +"' AND date >="+ str(date_last_month) +" ORDER BY date"
    stdev_st = get_stdev(sql)
    maximum_dd_st = get_mdd(sql)
    romad_st = get_romad(sql)
    volatility_risk_st = get_volatility_risk(sql, False, '')

    if wf_pct >= 0:
        signal_type = "buy"
        signal_dir = '<'
    else:
        signal_type = "sell"
        signal_dir = '<'

    signal_entry = signal_dir + str(round(float(last_price), decimal_places))
    date_next_week = last_date + timedelta(days=7)
    signal_expiration = date_next_week.strftime("%Y%m%d")
    risk_reward_ratio = 1.5

    buy_tp_gap_1 = float(trade_tp_buy_1) * float(volatility_risk_st) * float(risk_reward_ratio)
    buy_sl_gap_1 = float(trade_sl_buy_1) * float(volatility_risk_st)
    buy_tp_gap_2 = float(trade_tp_buy_2) * float(volatility_risk_st) * float(risk_reward_ratio)
    buy_sl_gap_2 = float(trade_sl_buy_2) * float(volatility_risk_st)
    sell_tp_gap_1 = float(trade_tp_sell_1) * float(volatility_risk_st) * float(risk_reward_ratio)
    sell_sl_gap_1 = float(trade_sl_sell_1) * float(volatility_risk_st)
    sell_tp_gap_2 = float(trade_tp_sell_2) * float(volatility_risk_st) * float(risk_reward_ratio)
    sell_sl_gap_2 = float(trade_sl_sell_2) * float(volatility_risk_st)

    trade_entry_buy_1 = round(float(trade_entry_buy_1), decimal_places)
    trade_tp_buy_1 = round(float(trade_tp_buy_1) + float(buy_tp_gap_1), decimal_places)
    trade_sl_buy_1 = round(float(trade_sl_buy_1) - float(buy_sl_gap_1), decimal_places)
    trade_entry_buy_2 = round(float(trade_entry_buy_2), decimal_places)
    trade_tp_buy_2 = round(float(trade_tp_buy_2) + float(buy_tp_gap_2), decimal_places)
    trade_sl_buy_2 = round(float(trade_sl_buy_2) - float(buy_sl_gap_2), decimal_places)
    trade_entry_sell_1 = round(float(trade_entry_sell_1), decimal_places)
    trade_tp_sell_1 = round(float(trade_tp_sell_1) - float(sell_tp_gap_1), decimal_places)
    trade_sl_sell_1 = round(float(trade_sl_sell_1) + float(sell_sl_gap_1), decimal_places)
    trade_entry_sell_2 = round(float(trade_entry_sell_2), decimal_places)
    trade_tp_sell_2 = round(float(trade_tp_sell_2) - float(sell_tp_gap_2), decimal_places)
    trade_sl_sell_2 = round(float(trade_sl_sell_2) + float(sell_sl_gap_2), decimal_places)

    if (trade_entry_buy_1 < 0 or trade_entry_buy_2 < 0 or
            trade_entry_sell_1 < 0 or trade_entry_sell_2 < 0):
        trade_entry_buy_1 = round(last_price, decimal_places)
        trade_entry_buy_2 = round(last_price, decimal_places)
        trade_entry_sell_1 = round(last_price, decimal_places)
        trade_entry_sell_2 = round(last_price, decimal_places)

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


    cr_i = connection.cursor(pymysql.cursors.SSCursor)
    sql_i = "UPDATE instruments SET y1="+str(y1_pct)+",m6="+str(m6_pct)+\
    ",m3="+str(m3_pct)+",m1="+str(m1_pct)+",w1="+str(w1_pct)+",d1="+\
    str(d1_pct)+",wf="+str(wf_pct)+","+\
    "signal_type='"+ signal_type +"',signal_entry='"+ signal_entry +\
    "',signal_expiration="+ str(signal_expiration) + ","+\
    "trade_1_entry="+str(trade_entry_buy_1)+",trade_1_tp="+str(trade_tp_buy_1)+\
    ",trade_1_sl="+str(trade_sl_buy_1)+",trade_1_type='buy',"+\
    "trade_2_entry="+str(trade_entry_buy_2)+",trade_2_tp="+str(trade_tp_buy_2)+\
    ",trade_2_sl="+str(trade_sl_buy_2)+",trade_2_type='buy',"+\
    "trade_3_entry="+str(trade_entry_sell_1)+",trade_3_tp="+str(trade_tp_sell_1)+\
    ",trade_3_sl="+str(trade_sl_sell_1)+",trade_3_type='sell',"+\
    "trade_4_entry="+str(trade_entry_sell_2)+",trade_4_tp="+str(trade_tp_sell_2)+\
    ",trade_4_sl="+str(trade_sl_sell_2)+",trade_4_type='sell', "+\
    "stdev_st="+ str(stdev_st)+", maximum_dd_st="+ str(maximum_dd_st)+", romad_st="+\
    str(romad_st) + ", volatility_risk_st="+ str(volatility_risk_st) +", "+\
    "y1_signal="+str(y1_pct_signal)+",m6_signal="+str(m6_pct_signal)+",m3_signal="+\
    str(m3_pct_signal)+",m1_signal="+str(m1_pct_signal)+",w1_signal="+str(w1_pct_signal) +", "+\
    "sentiment="+str(sentiment)+" "+\
    "WHERE symbol='"+symbol+"' "
    debug(sql_i)
    cr_i.execute(sql_i)
    connection.commit()
    cr_i.close()

def get_instr_sum(symbol, uid, asset_class, date_this, sentiment, connection):
    """
    Retrieve instrument data summary
    Args:
        String: Instrument symbol
        Integer: Instrument unique id
        String: Instrument asset class
        String: Date in string format YYYYMMDD
        Double: Instrument sentiment score
    Returns:
        None
    """
    mul = 1
    #Convert from percentage to pips for forex
    if asset_class == 'FX:':
        mul = 10000

    instr_data = InstrumentSummaryData(symbol, uid, connection)
    forc_data = ForecastData(uid, connection)
    # ---
    y1_pct_signal = float(instr_data.get_pct_1_year_signal())* mul
    m6_pct_signal = float(instr_data.get_pct_6_month_signal())* mul
    m3_pct_signal = float(instr_data.get_pct_3_month_signal())* mul
    m1_pct_signal = float(instr_data.get_pct_1_month_signal())* mul
    w1_pct_signal = float(instr_data.get_pct_1_week_signal())* mul

    y1_pct = float(instr_data.get_pct_1_year_performance())* mul
    m6_pct = float(instr_data.get_pct_6_month_performance())* mul
    m3_pct = float(instr_data.get_pct_3_month_performance())* mul
    m1_pct = float(instr_data.get_pct_1_month_performance())* mul
    w1_pct = float(instr_data.get_pct_1_week_performance())* mul
    d1_pct = float(instr_data.get_pct_1_day_performance())* mul
    frc_pt = forc_data.get_frc_pt()
    lp_pt = instr_data.get_last_price()
    wf_pct = 0
    if frc_pt != -9:
        weekf = get_forecast_pct(lp_pt, frc_pt)
        wf_pct = weekf * mul
    else:
        weekf = -999
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
    update_forecast_table(symbol, weekf, frc_pt, date_this, connection)
    update_instruments_table(symbol, y1_pct, m6_pct, m3_pct, m1_pct, w1_pct, d1_pct, wf_pct,
                             trade_entry_buy_1, trade_tp_buy_1, trade_sl_buy_1,
                             trade_entry_buy_2, trade_tp_buy_2, trade_sl_buy_2,
                             trade_entry_sell_1, trade_tp_sell_1, trade_sl_sell_1,
                             trade_entry_sell_2, trade_tp_sell_2, trade_sl_sell_2,
                             y1_pct_signal, m6_pct_signal, m3_pct_signal,
                             m1_pct_signal, w1_pct_signal, sentiment, connection)
