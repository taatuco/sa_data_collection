###############################################################################
# Desc: Transform and compute data for technical analysis
#
# This script prepare and collect technical analysis data to insert in the table
# price_instruments_data. Various scripts are called to calculate and transform data
# to import in the database.
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Date: July 5, 2018
###############################################################################
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

#import db access object
import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

#import all TA functions
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_data_collection\\ta_data\\"))
from ta_zeroing_fib_trend import *
from ta_calc_ma import *
from ta_calc_rsi import *
from ta_calc_l_h import *
from ta_calc_tln import *

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

try:
    with connection.cursor() as cr:
        sql = "SELECT symbol, r_quantmod FROM symbol_list ORDER BY symbol DESC"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            symbol_quantmod = row["r_quantmod"]
            symbol_id = row["symbol"]
            # for each symbol
            set_zero_fib_trend(symbol_id)

            with connection.cursor() as cr_d_id:
                sql_d_id = "SELECT id, date FROM price_instruments_data "+\
                "WHERE symbol='"+symbol_id+"' and is_ta_calc=0 ORDER BY date ASC"
                cr_d_id.execute(sql_d_id)
                rs_date_id = cr_d_id.fetchall()
                for row in rs_date_id:
                    date_id = str(row["date"]).replace("-","")
                    id = row["id"]
                    # for each symbol and each date
                    rsi = rsi_data(symbol_id,date_id,14)
                    lh = low_high_data(symbol_id, date_id, 20)
                    change_1d = rsi.get_change()
                    gain_1d = rsi.get_gain()
                    loss_1d = rsi.get_loss()
                    avg_gain = rsi.get_avg_gain()
                    avg_loss = rsi.get_avg_loss()
                    rs14 = rsi.get_rs()
                    rsi14 = rsi.get_rsi()
                    rsi_overbought = rsi.get_rsi_overbought()
                    rsi_oversold = rsi.get_rsi_oversold()
                    ma200 = calc_ma(symbol_id,date_id,200)
                    lowest_20d = lh.get_low()
                    highest_20d = lh.get_high()

                    is_ta_calc = "1"
                    # update record
                    try:
                        cr_upd = connection.cursor(pymysql.cursors.SSCursor)
                        sql_upd = "UPDATE price_instruments_data SET "+\
                        "change_1d="+str(change_1d)+", "+\
                        "gain_1d="+str(gain_1d)+", "+\
                        "loss_1d="+str(loss_1d)+", "+\
                        "avg_gain="+str(avg_gain)+", "+\
                        "avg_loss="+str(avg_loss)+", "+\
                        "rs14="+str(rs14)+", "+\
                        "rsi14="+str(rsi14)+", "+\
                        "rsi_overbought="+str(rsi_overbought)+", "+\
                        "rsi_oversold="+str(rsi_oversold)+", "+\
                        "ma200="+str(ma200)+ ", "+\
                        "lowest_20d="+str(lowest_20d)+", "+\
                        "highest_20d="+str(highest_20d)+", "+\
                        "is_ta_calc="+str(is_ta_calc)+" "+\
                        "WHERE id="+str(id)
                        cr_upd.execute(sql_upd)
                        connection.commit()
                        cr_upd.close()
                    except:
                        sql_upd = "UPDATE price_instruments_data SET "+\
                        "is_ta_calc=1 "+\
                        "WHERE id="+str(id)
                        cr_upd.execute(sql_upd)
                        connection.commit()
                        cr_upd.close()

            # Calc trend line
            get_trend_line_data(symbol_id)
            
            cr_d_id.close()
finally:
    connection.close()
