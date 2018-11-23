# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
import csv
from pathlib import Path

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

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def get_rsi_mom(os,ob,we,sg,lt_rsi_mom):

    r = ''
    if (lt_rsi_mom.lower() == 'overbought'):
        r = ob
    if (lt_rsi_mom.lower() == 'oversold'):
        r = os
    if (lt_rsi_mom.lower() == 'weak'):
        r = we
    if (lt_rsi_mom.lower() == 'strong'):
        r = sg

    return r


def gen_recomm(s,uid):

    try:
        wf = 0
        buy_entry = 0
        buy_tp = 0
        buy_sl = 0
        sell_entry = 0
        sell_tp = 0
        sell_sl = 0
        ma200 = 0
        st_upper_range = 0
        st_lower_range = 0
        lt_rsi_avg = 0
        lt_rsi_mom = ''
        last_price = 0
        decimal_places = 0

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT decimal_places FROM instruments WHERE symbol='"+s+"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            decimal_places = int(row[0])

        data_src = sett.get_path_src()
        ext = ".csv"
        f = data_src+str(uid)+'s.csv'
        filepath = Path(f)
        if filepath.exists():
            with open(f) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                i = 1
                for row in readCSV:
                    if (i == 2):
                        wf = float(row[5])
                        buy_entry = round(float(row[6]), decimal_places)
                        buy_tp = round(float(row[7]), decimal_places)
                        buy_sl = round(float(row[8]), decimal_places)
                        sell_entry = round(float(row[14]), decimal_places)
                        sell_tp = round(float(row[15]), decimal_places)
                        sell_sl = round(float(row[16]), decimal_places)
                    i +=1

        f = data_src+str(uid)+'t.csv'
        filepath = Path(f)
        if filepath.exists():
            with open(f) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                i = 1
                for row in readCSV:
                    if (i == 2):
                        ma200 = float(row[18])
                        st_upper_range = float(row[11])
                        st_lower_range = float(row[10])
                        lt_rsi_avg = row[14]
                        lt_rsi_mom = row[17]
                    i +=1

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT price_close FROM price_instruments_data WHERE symbol='"+s+"' ORDER BY date DESC LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            last_price = row[0]


        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT * FROM recommendations"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            lang = row[0]
            price_under_200ma = row[1]
            price_above_200ma = row[2]
            st_upper_range_above_price_range = row[3]
            st_lower_range_below_price_range = row[4]
            upper_range_below_price_downtrend = row[5]
            lower_range_above_price_uptrend = row[6]
            rsi_oversold = row[7]
            rsi_overbought = row[8]
            rsi_weak = row[9]
            rsi_strong = row[10]
            uptrend_recomm = row[11]
            downtrend_recomm = row[12]

            pt1 = ''
            pt2 = ''
            pt3 = ''
            pt4 = ''
            pt5 = ''

            if (last_price < ma200):
                pt1 = price_under_200ma
            if (last_price > ma200):
                pt1 = price_above_200ma
            if (st_upper_range > last_price):
                pt2 = st_upper_range_above_price_range
            if (st_lower_range < last_price):
                pt2 = st_lower_range_below_price_range
            if (st_upper_range < last_price and wf < 0):
                pt3 = upper_range_below_price_downtrend
            if (st_lower_range > last_price and wf >= 0):
                pt3 = lower_range_above_price_uptrend
            pt4 = get_rsi_mom(rsi_oversold,rsi_overbought,rsi_weak,rsi_strong,lt_rsi_mom)
            if (wf < 0):
                pt5 = downtrend_recomm
            else:
                pt5 = uptrend_recomm

            pt1 = pt1.replace("{symbol}",s)
            pt2 = pt2.replace("{st_upper_range}",str(st_upper_range) )
            pt2 = pt2.replace("{st_lower_range}",str(st_lower_range) )
            pt3 = pt3.replace("{symbol}",s)
            pt3 = pt3.replace("{st_upper_range}",str(st_upper_range) )
            pt3 = pt3.replace("{st_lower_range}",str(st_lower_range) )
            pt4 = pt4.replace("{symbol}",s)
            pt4 = pt4.replace("{rsi_50_day_avg}",str(round(float(lt_rsi_avg),2) ) )
            pt5 = pt5.replace("{symbol}",s)
            pt5 = pt5.replace("{buy_entry}", str(buy_entry) )
            pt5 = pt5.replace("{buy_target_price}",  str(buy_tp)  )
            pt5 = pt5.replace("{buy_stop_loss}", str(buy_sl) )
            pt5 = pt5.replace("{sell_entry}", str(sell_entry)  )
            pt5 = pt5.replace("{sell_target_price}", str(sell_tp) )
            pt5 = pt5.replace("{sell_stop_loss}", str(sell_sl)  )


            r = pt1 + " " + pt2 + " " + pt3 + " " + pt4 + " " + pt5

            f = sett.get_path_src()+"\\"+str(uid)+lang+"r.csv"
            with open(f, 'w', newline='') as csvfile:
                fieldnames = ["recomm"]

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({"recomm": str(r)})


        print(str(uid) +": "+ os.path.basename(__file__) )

    except Exception as e: print(e)
