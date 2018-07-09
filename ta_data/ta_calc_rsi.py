# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

'''
(FIRST_AVG, GAIN, LOSS) = AVERAGE( (GAIN) ), AVERAGE( (LOSS) ) (if count> rsi_period)
(AVG_GAIN) = ( (PREVIOUS_AVG_GAIN)*(rsi_period-1)+ (GAIN) ) / rsi_period
(AVG_LOSS) = ( (PREVIOUS_AVG_LOSS)*(rsi_period-1)+ (LOSS) ) / rsi_period
(RS) = (AVG_GAIN) / (AVG_LOSS)
(RSI) = if( (RS)=0, 100, 100-(100/1+(RS)) )
'''
class day_data:

    c_prev_avg_gain = 0
    c_prev_price_close = 0
    c_curr_price_close = 0
    c_change_1d = 0
    c_prev_avg_gain = 0
    c_prev_avg_loss = 0
    c_curr_avg_gain = 0
    c_curr_avg_loss = 0

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

 
    def __init__(self, symbol_id, date_id, rsi_period):
        self.symbol = symbol_id
        self.date = date_id
        self.rsi_period = rsi_period
    
    def get_gain(self):
        gain_1d = 0
        if day_data.c_change_1d >= 0:
            gain_1d = day_data.c_change_1d
        return gain_1d

    def get_avg_gain(self):
        #(FIRST_AVG, GAIN, LOSS) = AVERAGE( (GAIN) ), AVERAGE( (LOSS) ) (if count> rsi_period)
        # In case previous is 0 then get average of last rsi_period
        tt_gain = 0
        if day_data.c_prev_avg_gain == 0:
            with day_data.connection.cursor() as cr_get_avg:
                sql_get_avg = "SELECT avg_gain, gain_1d FROM price_instruments_data "+\
                              "WHERE symbol='"+self.symbol+"' AND date<"+str(self.date)+" "+\
                              "LIMIT "+str(self.rsi_period)
                cr_get_avg.execute(sql_get_avg)
                result_avg = cr_get_avg.fetchall()
                if cr_get_avg.rowcount == self.rsi_period:
                    for row in result_avg:
                        tt_gain = tt_gain + row["gain_1d"]
                    day_data.c_curr_avg_gain = tt_gain / self.rsi_period
                    
        return day_data.c_curr_avg_gain

    def get_loss(self):
        loss_1d = 0    
        if day_data.c_change_1d < 0:
            loss_1d = (day_data.c_change_1d)*(-1)
        return loss_1d

    def get_change(self):
        day_data.c_change_1d = day_data.c_curr_price_close - day_data.c_prev_price_close
        return day_data.c_change_1d
    
    def set_data(self):
        with day_data.connection.cursor() as cr_get_prev_d:
            sql_get_prev_d = "SELECT price_close, avg_gain, avg_loss FROM price_instruments_data "+\
                                 "WHERE symbol='"+self.symbol+"' AND date<"+str(self.date)+" "+\
                                 "ORDER BY date DESC LIMIT 1"
            cr_get_prev_d.execute(sql_get_prev_d)
            result_prev = cr_get_prev_d.fetchall()
            if result_prev:
                for row in result_prev:
                    day_data.c_prev_close_price = row["price_close"]
                    day_data.c_prev_avg_gain = row["avg_gain"]
                    day_data.c_prev_avg_loss = row["avg_loss"]
                           
                with day_data.connection.cursor() as cr_get_curr_d:
                    sql_get_curr_d = "SELECT price_close, avg_gain, avg_loss FROM price_instruments_data "+\
                                         "WHERE symbol='"+self.symbol+"' AND date="+str(self.date)+" "+\
                                         "ORDER BY date DESC LIMIT 1"
                    cr_get_curr_d.execute(sql_get_curr_d)
                    result_curr = cr_get_curr_d.fetchall()
                    if result_curr:
                        for row in result_curr:
                            day_data.c_curr_price_close = row["price_close"]
                            day_data.c_curr_avg_gain = row["avg_gain"]
                            day_data.c_curr_avg_loss = row["avg_loss"]
                            
                    cr_get_curr_d.close()
            cr_get_prev_d.close()

def calc_rsi(symbol_id, date_id, rsi_period):
        rsi_period = rsi_period
        d = day_data(symbol_id, date_id, rsi_period)
        d.set_data()
        change_1d = d.get_change()
        gain_1d = d.get_gain()
        loss_1d = d.get_loss()
        avg_gain = d.get_avg_gain()

        print(str(change_1d) +" "+ str(gain_1d) +" "+str(loss_1d)+ " "+ str(avg_gain) )
        del d
