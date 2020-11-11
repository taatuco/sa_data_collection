""" Functionalities related to chart """
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
from sa_numeric import get_pct_change
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def get_trade_pnl(uid, date_this, connection):
    """
    Collect trade profit and loss
    Args:
        Integer: Trade unique ID
        String: Date in string format YYYYMMDD, expiration date.
    Returns:
        Double: trade profit and loss
    """
    ret = 0
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT pnl_pct FROM trades WHERE uid=" + str(uid) +\
    " AND expiration_date = "+ str(date_this)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    cursor.close()
    return ret

def clear_chart_table(symbol, connection):
    """
    Remove the content of chart_data table
    Args:
        String: Instrument symbol
    Returns:
        None
    """
    if symbol != '':
        sql = 'DELETE FROM chart_data WHERE symbol LIKE "'+ str(symbol) +'"'
    else:
        sql = 'TRUNCATE chart_data'

    cr_t = connection.cursor(pymysql.cursors.SSCursor)
    sql_t = sql
    debug(sql_t)
    cr_t.execute(sql_t)
    connection.commit()
    cr_t.close()

def gen_chart(symbol, uid, connection):
    """
    Generate chart data
    Args:
        String: Instrument symbol
        Integer: Instrument unique id
    Returns:
        None
    """
    decimal_places = 2
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT decimal_places FROM instruments WHERE symbol='"+symbol+"'"
    debug(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        decimal_places = int(row[0])
    cursor.close()

    date_today = datetime.datetime.today()
    date_start = date_today - (timedelta(days=400))
    long_term = date_today - (timedelta(days=360))
    short_term = date_today - (timedelta(days=180))

    date_start = date_start.strftime("%Y%m%d")


    data_src = SETT.get_path_src()
    file_this = data_src+str(uid)+'t.csv'
    filepath = Path(file_this)
    if filepath.exists():
        with open(file_this) as csvfile:
            csv_file = csv.reader(csvfile, delimiter=',')
            i = 1
            for row in csv_file:
                if i == 2:
                    st_sd = short_term.strftime("%Y-%m-%d")
                    st_sd = row[0]
                    st_slope_low = row[1]
                    st_slope_high = row[2]
                    lt_sd = long_term.strftime("%Y-%m-%d")
                    lt_slope_low = row[4]
                    lt_slope_high = row[5]
                    st_sdv_low = row[6]
                    st_sdv_high = row[7]
                    lt_sdv_low = row[8]
                    lt_sdv_high = row[9]
                debug(str(row[0])+':::'+str(row[2])+':::'+str(row[3])+':::'+\
                      str(row[4])+':::'+str(row[5]))
                i += 1

        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT date, price_close, ma200, rsi14, rsi_overbought, "+\
        "rsi_oversold, target_price "+\
        "FROM price_instruments_data WHERE symbol='"+symbol+"' AND date>=" +\
        date_start + " ORDER BY date"
        debug(sql)
        cursor.execute(sql)
        res = cursor.fetchall()

        lt_lower_trend_line = '0'
        lt_upper_trend_line = '0'
        draw_lt = False
        st_lower_trend_line = '0'
        st_upper_trend_line = '0'
        draw_st = False
        pct_change = 0
        ini_signal = 0
        signal_price = 0
        pct_signal = 0
        trade_pct = 0

        i = 0
        inserted_values = ''

        for row in res:
            date = row[0]
            price = float(round(row[1], decimal_places))
            ma200 = float(round(row[2], decimal_places))
            rsi = float(round(row[3], 2))
            rsi_overbought = float(round(row[4], 2))
            rsi_oversold = float(round(row[5], 2))
            target_price = float(round(row[6], decimal_places))

            date_compare = datetime.datetime.combine(date, datetime.datetime.min.time())

            if  date_compare >= datetime.datetime.strptime(lt_sd, '%Y-%m-%d') and not draw_lt:
                lt_lower_trend_line = lt_sdv_low
                lt_upper_trend_line = lt_sdv_high
                draw_lt = True

            if date_compare >= datetime.datetime.strptime(st_sd, '%Y-%m-%d') and not draw_st:
                st_lower_trend_line = st_sdv_low
                st_upper_trend_line = st_sdv_high
                draw_st = True

            if draw_lt:
                lt_lower_trend_line = str(round(float(lt_lower_trend_line) +
                                                float(lt_slope_low), decimal_places))
                lt_upper_trend_line = str(round(float(lt_upper_trend_line) +
                                                float(lt_slope_high), decimal_places))

            if draw_st:
                st_lower_trend_line = str(round(float(st_lower_trend_line) +
                                                float(st_slope_low), decimal_places))
                st_upper_trend_line = str(round(float(st_upper_trend_line) +
                                                float(st_slope_high), decimal_places))

            if i == 0:
                ini_val = price
                pct_change = 0
                signal_price = price
                ini_signal = signal_price
                pct_signal = 0
                sep = ''
            else:
                trade_pct = float(get_trade_pnl(uid, date.strftime("%Y%m%d"), connection))/5
                if trade_pct > 0:
                    trade_pct * 1.5

                pct_change = get_pct_change(ini_val, price)
                signal_price = (signal_price +
                                (signal_price * trade_pct))
                pct_signal = get_pct_change(ini_signal, signal_price)
                sep = ','

            inserted_values = inserted_values + sep +\
            "("+str(uid)+\
            ",'"+str(symbol)+\
            "',"+str(date.strftime("%Y%m%d"))+\
            ","+str(price)+",'0',"+\
            str(lt_upper_trend_line)+\
            ","+str(lt_lower_trend_line)+\
            ","+str(st_upper_trend_line)+\
            ","+str(st_lower_trend_line)+\
            ","+str(rsi)+\
            ","+str(rsi_oversold)+\
            ","+str(rsi_overbought)+\
            ","+str(ma200)+\
            ","+str(target_price)+\
            ","+str(pct_change)+\
            ","+ str(signal_price)+\
            ","+ str(pct_signal) +")"

            debug(inserted_values)
            i += 1

        cr_t = connection.cursor(pymysql.cursors.SSCursor)
        sql_t = "INSERT IGNORE INTO chart_data(uid, symbol, date, price_close, forecast, "+\
        "lt_upper_trend_line, lt_lower_trend_line, "+\
        "st_upper_trend_line, st_lower_trend_line, "+\
        "rsi, rsi_oversold, rsi_overbought, ma200, "+\
        "target_price, percent_perf, signal_price, percent_signal) VALUES "+ inserted_values
        debug(sql_t +": "+str(uid)+"> "+str(date)+": "+ os.path.basename(__file__))
        cr_t.execute(sql_t)
        connection.commit()
        cr_t.close()
        cursor.close()

        file_this = data_src+str(uid)+'f.csv'
        filepath = Path(file_this)
        if filepath.exists():
            with open(file_this) as csvfile:
                csv_file = csv.reader(csvfile, delimiter=',')
                i = 1
                inserted_values = ''
                for row in csv_file:
                    forecast = '0'
                    if i >= 2:
                        date = date + (timedelta(days=1))
                        forecast = row[1]
                        lt_lower_trend_line = str(round(float(lt_lower_trend_line) +
                                                        float(lt_slope_low), decimal_places))
                        lt_upper_trend_line = str(round(float(lt_upper_trend_line) +
                                                        float(lt_slope_high), decimal_places))
                        st_lower_trend_line = str(round(float(st_lower_trend_line) +
                                                        float(st_slope_low), decimal_places))
                        st_upper_trend_line = str(round(float(st_upper_trend_line) +
                                                        float(st_slope_high), decimal_places))

                    sep = ''
                    if i > 2:
                        sep = ','

                    if i == 8:
                        cr_fp = connection.cursor(pymysql.cursors.SSCursor)
                        sql_fp = "SELECT target_price FROM price_instruments_data "+\
                        "WHERE symbol = '"+ str(symbol) +"' ORDER BY date DESC LIMIT 1"
                        debug(sql_fp)
                        cr_fp.execute(sql_fp)
                        rs_fp = cr_fp.fetchall()
                        for row in rs_fp:
                            forecast = row[0]
                        cr_fp.close()

                    if forecast != '':
                        if float(forecast) > 0:
                            if inserted_values == '':
                                sep = ''
                            inserted_values = inserted_values + sep +\
                            "("+str(uid)+",'"+\
                            str(symbol)+"',"+\
                            str(date.strftime("%Y%m%d"))+","+\
                            str(price)+","+\
                            str(forecast)+","+\
                            str(lt_upper_trend_line)+","+\
                            str(lt_lower_trend_line)+","+\
                            str(st_upper_trend_line)+","+\
                            str(st_lower_trend_line)+","+\
                            str(rsi)+","+\
                            str(rsi_oversold)+","+\
                            str(rsi_overbought)+","+\
                            str(ma200)+","+\
                            str(target_price)+")"
                    i += 1
                if inserted_values != '':
                    cr_t = connection.cursor(pymysql.cursors.SSCursor)
                    sql_t = "INSERT IGNORE INTO chart_data(uid, symbol, "+\
                    "date, price_close, forecast, "+\
                    "lt_upper_trend_line, lt_lower_trend_line, "+\
                    "st_upper_trend_line, st_lower_trend_line, "+\
                    "rsi, rsi_oversold, rsi_overbought, ma200, target_price) VALUES "+\
                    inserted_values
                    debug(sql_t +": "+str(uid)+"> "+str(date)+": "+ os.path.basename(__file__))
                    cr_t.execute(sql_t)
                    connection.commit()
                    cr_t.close()
