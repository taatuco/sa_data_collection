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
from get_pct_change import *


pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def gen_chart(s,uid):

    decimal_places = 2
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT decimal_places FROM instruments WHERE symbol='"+s+"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        decimal_places = int(row[0])



    n = datetime.datetime.today()
    d = n - ( timedelta(days=365) )
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
                    except Exception as e: print(e)

                i +=1

        cr_t = connection.cursor(pymysql.cursors.SSCursor)
        sql_t = "DELETE FROM chart_data WHERE uid=" + str(uid)
        cr_t.execute(sql_t)
        connection.commit()

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT date, price_close, ma200, rsi14, rsi_overbought, rsi_oversold, target_price "+\
        "FROM price_instruments_data WHERE symbol='"+s+"' AND date>=" + d + " ORDER BY date"
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

        i = 0

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
            else:
                pct_change = get_pct_change(ini_val, price)


            sql_t = "INSERT INTO chart_data(uid, symbol, date, price_close, forecast, "+\
            "lt_upper_trend_line, lt_lower_trend_line, "+\
            "st_upper_trend_line, st_lower_trend_line, "+\
            "rsi, rsi_oversold, rsi_overbought, ma200, target_price, percent_perf) "+\
            "VALUES ("+str(uid)+",'"+str(s)+"',"+str(date.strftime("%Y%m%d"))+","+str(price)+",'0',"+\
            str(lt_upper_trend_line)+","+str(lt_lower_trend_line)+","+\
            str(st_upper_trend_line)+","+st_lower_trend_line+","+\
            str(rsi)+","+str(rsi_oversold)+","+str(rsi_overbought)+","+str(ma200)+","+str(target_price)+","+str(pct_change) +")"
            print(sql_t +": "+str(uid)+"> "+str(date)+": "+ os.path.basename(__file__) )
            cr_t.execute(sql_t)
            connection.commit()
            i += 1

        f = data_src+str(uid)+'f.csv'
        filepath = Path(f)
        if filepath.exists():
            with open(f) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                i = 1
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

                        sql_t = "INSERT INTO chart_data(uid, symbol, date, price_close, forecast, "+\
                        "lt_upper_trend_line, lt_lower_trend_line, "+\
                        "st_upper_trend_line, st_lower_trend_line, "+\
                        "rsi, rsi_oversold, rsi_overbought, ma200, target_price) "+\
                        "VALUES ("+str(uid)+",'"+str(s)+"',"+str(date.strftime("%Y%m%d"))+","+str(price)+","+str(forecast)+","+\
                        str(lt_upper_trend_line)+","+str(lt_lower_trend_line)+","+\
                        str(st_upper_trend_line)+","+st_lower_trend_line+","+\
                        str(rsi)+","+str(rsi_oversold)+","+str(rsi_overbought)+","+str(ma200)+","+str(target_price)+")"
                        print(sql_t +": "+str(uid)+"> "+str(date)+": "+ os.path.basename(__file__) )
                        cr_t.execute(sql_t)
                        connection.commit()

                    i +=1
