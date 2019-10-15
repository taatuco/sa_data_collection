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
from sa_numeric import *


pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_trade_pnl(uid,d):
    r = 0
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT pnl_pct FROM trades WHERE uid=" + str(uid) + " AND expiration_date = "+ str(d)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
    except Exception as e: debug(e)
    return r

def clear_chart_table(s):
    try:

        if s == '' or s == None:
            sql = 'DELETE FROM chart_data WHERE symbol LIKE "'+ str(s) +'"'
        else:
            sql = 'TRUNCATE chart_data'

        cr_t = connection.cursor(pymysql.cursors.SSCursor)
        sql_t = sql
        debug(sql_t)
        cr_t.execute(sql_t)
        connection.commit()
        cr_t.close()

    except Exception as e: debug(e)

def gen_chart(s,uid):

    try:
        decimal_places = 2
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT decimal_places FROM instruments WHERE symbol='"+s+"'"
        debug(sql)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            decimal_places = int(row[0])
        cr.close()


        n = datetime.datetime.today()
        d = n - ( timedelta(days=400) )
        lt = n - ( timedelta(days=360) )
        st = n - ( timedelta(days=180) )

        d = d.strftime("%Y%m%d")


        data_src = sett.get_path_src()
        ext = ".csv"
        f = data_src+str(uid)+'t.csv'
        filepath = Path(f)
        if filepath.exists():
            with open(f) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                i = 1
                for row in readCSV:
                    if (i == 2):
                        try:
                            wf = float(row[5])
                            buy_entry = round(float(row[6]), decimal_places)
                            st_sd = st.strftime("%Y-%m-%d")
                            st_sd = row[0]
                            st_slope_low = row[1]
                            st_slope_high = row[2]
                            lt_sd = lt.strftime("%Y-%m-%d")
                            lt_slope_low = row[4]
                            lt_slope_high = row[5]
                            st_sdv_low = row[6]
                            st_sdv_high = row[7]
                            lt_sdv_low = row[8]
                            lt_sdv_high = row[9]
                            st_lower_range = row[10]
                            st_upper_range = row[11]
                            lt_lower_range = row[12]
                            lt_upper_range = row[13]
                        except Exception as e: debug(e)
                    debug( str(row[0])+':::'+str(row[2])+':::'+str(row[3])+':::'+str(row[4])+':::'+str(row[5]) )
                    i +=1

            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT date, price_close, ma200, rsi14, rsi_overbought, rsi_oversold, target_price "+\
            "FROM price_instruments_data WHERE symbol='"+s+"' AND date>=" + d + " ORDER BY date"
            debug(sql)
            cr.execute(sql)
            rs = cr.fetchall()

            lt_lower_trend_line = '0'
            lt_upper_trend_line = '0'
            draw_lt = False
            st_lower_trend_line = '0'
            st_upper_trend_line = '0'
            draw_st = False
            ini_price = 0
            pct_change = 0
            ini_signal = 0
            signal_price = 0
            pct_signal = 0

            i = 0
            inserted_values = ''

            for row in rs:

                title = '1Y - '+ s
                date = row[0]
                price = float( round(row[1], decimal_places) )
                ma200 = float( round(row[2], decimal_places) )
                rsi = float( round(row[3], 2) )
                rsi_overbought = float( round(row[4], 2) )
                rsi_oversold = float( round(row[5], 2) )
                target_price = float( round(row[6], decimal_places) )

                if (datetime.datetime.combine(date, datetime.datetime.min.time())  >= datetime.datetime.strptime(lt_sd, '%Y-%m-%d') and not draw_lt) :
                    lt_lower_trend_line = lt_sdv_low
                    lt_upper_trend_line = lt_sdv_high
                    draw_lt = True

                if (datetime.datetime.combine(date, datetime.datetime.min.time()) >= datetime.datetime.strptime(st_sd, '%Y-%m-%d') and not draw_st ):
                    st_lower_trend_line = st_sdv_low
                    st_upper_trend_line = st_sdv_high
                    draw_st = True

                if (draw_lt):
                    try:
                        lt_lower_trend_line = str( round( float(lt_lower_trend_line) + float(lt_slope_low), decimal_places) )
                        lt_upper_trend_line = str( round( float(lt_upper_trend_line) + float(lt_slope_high), decimal_places) )
                    except:
                        lt_lower_trend_line = '0'
                        lt_upper_trend_line = '0'

                if (draw_st):
                    try:
                        st_lower_trend_line = str( round( float(st_lower_trend_line) + float(st_slope_low), decimal_places) )
                        st_upper_trend_line = str( round( float(st_upper_trend_line) + float(st_slope_high), decimal_places) )
                    except:
                        st_lower_trend_line = '0'
                        st_upper_trend_line = '0'

                if i == 0:
                    ini_val = price
                    pct_change = 0
                    signal_price = price
                    ini_signal = signal_price
                    pct_signal = 0
                    sep = ''
                else:
                    pct_change = get_pct_change(ini_val, price)
                    signal_price =  signal_price + ( signal_price * float( get_trade_pnl(uid, date.strftime("%Y%m%d") ) ) )
                    pct_signal = get_pct_change(ini_signal, signal_price)
                    sep = ','

                inserted_values = inserted_values + sep +\
                "("+str(uid)+",'"+str(s)+"',"+str(date.strftime("%Y%m%d"))+","+str(price)+",'0',"+\
                str(lt_upper_trend_line)+","+str(lt_lower_trend_line)+","+\
                str(st_upper_trend_line)+","+st_lower_trend_line+","+\
                str(rsi)+","+str(rsi_oversold)+","+str(rsi_overbought)+","+str(ma200)+","+str(target_price)+","+\
                str(pct_change)+","+ str(signal_price) +","+ str(pct_signal) +")"

                debug(inserted_values)
                i += 1

            cr_t = connection.cursor(pymysql.cursors.SSCursor)
            sql_t = "INSERT IGNORE INTO chart_data(uid, symbol, date, price_close, forecast, "+\
            "lt_upper_trend_line, lt_lower_trend_line, "+\
            "st_upper_trend_line, st_lower_trend_line, "+\
            "rsi, rsi_oversold, rsi_overbought, ma200, target_price, percent_perf, signal_price, percent_signal) VALUES "+ inserted_values
            debug(sql_t +": "+str(uid)+"> "+str(date)+": "+ os.path.basename(__file__) )
            cr_t.execute(sql_t)
            connection.commit()
            cr_t.close()
            cr.close()

            f = data_src+str(uid)+'f.csv'
            filepath = Path(f)
            if filepath.exists():
                with open(f) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=',')
                    i = 1
                    inserted_values = ''
                    forecast = '0'
                    for row in readCSV:
                        if (i >= 2):
                            date = date +  ( timedelta(days=1) )
                            forecast = row[1]
                            try:
                                lt_lower_trend_line = str( round( float(lt_lower_trend_line) + float(lt_slope_low), decimal_places) )
                                lt_upper_trend_line = str( round( float(lt_upper_trend_line) + float(lt_slope_high), decimal_places) )
                            except:
                                lt_lower_trend_line = '0'
                                lt_upper_trend_line = '0'

                            try:
                                st_lower_trend_line = str( round( float(st_lower_trend_line) + float(st_slope_low), decimal_places) )
                                st_upper_trend_line = str( round( float(st_upper_trend_line) + float(st_slope_high), decimal_places) )
                            except:
                                st_lower_trend_line = '0'
                                st_upper_trend_line = '0'

                        if i == 1:
                            sep = ''
                        else:
                            sep = ','

                        if i == 8:
                            cr_fp = connection.cursor(pymysql.cursors.SSCursor)
                            sql_fp = "SELECT target_price FROM price_instruments_data WHERE symbol = '"+ str(s) +"' ORDER BY date DESC LIMIT 1"
                            debug(sql_fp)
                            cr_fp.execute(sql_fp)
                            rs_fp = cr_fp.fetchall()
                            for row in rs_fp: forecast = str(row[0])
                            cr_fp.close()

                        inserted_values = inserted_values + sep +\
                        "("+str(uid)+",'"+str(s)+"',"+str(date.strftime("%Y%m%d"))+","+str(price)+","+str(forecast)+","+\
                        str(lt_upper_trend_line)+","+str(lt_lower_trend_line)+","+\
                        str(st_upper_trend_line)+","+st_lower_trend_line+","+\
                        str(rsi)+","+str(rsi_oversold)+","+str(rsi_overbought)+","+str(ma200)+","+str(target_price)+")"

                        i +=1

                    cr_t = connection.cursor(pymysql.cursors.SSCursor)
                    sql_t = "INSERT IGNORE INTO chart_data(uid, symbol, date, price_close, forecast, "+\
                    "lt_upper_trend_line, lt_lower_trend_line, "+\
                    "st_upper_trend_line, st_lower_trend_line, "+\
                    "rsi, rsi_oversold, rsi_overbought, ma200, target_price) VALUES "+ inserted_values
                    debug(sql_t +": "+str(uid)+"> "+str(date)+": "+ os.path.basename(__file__) )
                    cr_t.execute(sql_t)
                    connection.commit()
                    cr_t.close()

    except Exception as e: debug(e)
