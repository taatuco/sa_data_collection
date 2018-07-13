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

# Licensed under The MIT License
# Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

#define database username and password and other variable regarding access to db
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()


# Use PyMySQL to access MySQL database
import pymysql.cursors

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = "SELECT symbol, r_quantmod FROM symbol_list"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            symbol_quantmod = row["r_quantmod"]
            symbol_index = row["symbol"]
            # for each symbol
            set_zero_fib_trend(symbol_index)

            with connection.cursor() as cursor_date_index:
                sql_date_index = "SELECT id, date FROM price_instruments_data "+\
                "WHERE symbol='"+symbol_index+"' and is_ta_calc=0 ORDER BY date ASC"
                cursor_date_index.execute(sql_date_index)
                result_date_index = cursor_date_index.fetchall()
                for row in result_date_index:
                    date_index = str(row["date"]).replace("-","")
                    id = row["id"]
                    # for each symbol and each date
                    rsi = rsi_data(symbol_index,date_index,14)
                    change_1d = rsi.get_change()
                    gain_1d = rsi.get_gain()
                    loss_1d = rsi.get_loss()
                    avg_gain = rsi.get_avg_gain()
                    avg_loss = rsi.get_avg_loss()
                    rs14 = rsi.get_rs()
                    rsi14 = rsi.get_rsi()
                    rsi_overbought = rsi.get_rsi_overbought()
                    rsi_oversold = rsi.get_rsi_oversold()
                    ma200 = calc_ma(symbol_index,date_index,200)                    
                    is_ta_calc = "1"
                    
                    # update record
                    try:                        
                        cursor_update = connection.cursor(pymysql.cursors.SSCursor)
                        sql_update = "UPDATE price_instruments_data SET "+\
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
                        "is_ta_calc="+str(is_ta_calc)+" "+\
                        "WHERE id="+str(id)
                        #print(sql_update)
                        cursor_update.execute(sql_update)                    
                        connection.commit()
                        cursor_update.close()
                    except:
                        sql_update = "UPDATE price_instruments_data SET "+\
                        "is_ta_calc=1 "+\
                        "WHERE id="+str(id)
                        #print(sql_update)
                        cursor_update.execute(sql_update)                    
                        connection.commit()                        
                        cursor_update.close()

            cursor_date_index.close()
finally:
    connection.close()
