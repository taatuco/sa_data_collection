# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

#define database username and password and other variable regarding access to db
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

# Notes:
#
# Retrieve data in this order is recomended.
#
# rsi = rsi_data()
# change_1d = rsi.get_change()
# gain_1d = rsi.get_gain()
# loss_1d = rsi.get_loss()
# avg_gain = rsi.get_avg_gain()
# avg_loss = rsi.get_avg_loss()
# rs = rsi.get_rs()
# rsi = rsi.get_rsi()
# ...
#

class rsi_data:
    c_curr_gain = 0
    c_curr_loss = 0
    c_prev_price_close = 0
    c_curr_price_close = 0
    c_change_1d = 0
    c_prev_avg_gain = 0
    c_prev_avg_loss = 0
    c_curr_avg_gain = 0
    c_curr_avg_loss = 0
    c_prev_is_ta_calc = 0
    c_curr_is_ta_calc = 0
    c_rs = 0
    c_rsi = 0

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

        with rsi_data.connection.cursor() as cr_get_prev_d:
            sql_get_prev_d = "SELECT price_close, avg_gain, avg_loss, is_ta_calc FROM price_instruments_data "+\
                                 "WHERE symbol='"+self.symbol+"' AND date<"+str(self.date)+" "+\
                                 "ORDER BY date DESC LIMIT 1"
            cr_get_prev_d.execute(sql_get_prev_d)
            result_prev = cr_get_prev_d.fetchall()
            if result_prev:
                for row in result_prev:
                    rsi_data.c_prev_price_close = row["price_close"]
                    rsi_data.c_prev_avg_gain = row["avg_gain"]
                    rsi_data.c_prev_avg_loss = row["avg_loss"]
                    rsi_data.c_prev_is_ta_calc = row["is_ta_calc"]
                           
                with rsi_data.connection.cursor() as cr_get_curr_d:
                    sql_get_curr_d = "SELECT price_close, avg_gain, avg_loss, is_ta_calc FROM price_instruments_data "+\
                                         "WHERE symbol='"+self.symbol+"' AND date="+str(self.date)+" "+\
                                         "ORDER BY date DESC LIMIT 1"
                    cr_get_curr_d.execute(sql_get_curr_d)
                    result_curr = cr_get_curr_d.fetchall()
                    if result_curr:
                        for row in result_curr:
                            rsi_data.c_curr_price_close = row["price_close"]
                            rsi_data.c_curr_avg_gain = row["avg_gain"]
                            rsi_data.c_curr_avg_loss = row["avg_loss"]
                            rsi_data.c_curr_is_ta_calc = row["is_ta_calc"]
                            
                    cr_get_curr_d.close()
            cr_get_prev_d.close()        
    
    def get_gain(self):
        gain_1d = 0
        if rsi_data.c_change_1d >= 0:
            gain_1d = rsi_data.c_change_1d
        rsi_data.c_curr_gain = gain_1d
        return gain_1d

    def get_avg_gain(self):
        #(FIRST_AVG, GAIN, LOSS) = AVERAGE( (GAIN) ), AVERAGE( (LOSS) ) (if count> rsi_period)
        # In case previous is 0 then get average of last rsi_period
        tt_gain = 0
        if rsi_data.c_prev_avg_gain == 0:
            with rsi_data.connection.cursor() as cr_get_avg_g:
                sql_get_avg_g = "SELECT avg_gain, gain_1d FROM price_instruments_data "+\
                              "WHERE symbol='"+self.symbol+"' AND date<"+str(self.date)+" AND is_ta_calc=1 "+\
                              "LIMIT "+str(self.rsi_period)
                cr_get_avg_g.execute(sql_get_avg_g)
                result_avg_g = cr_get_avg_g.fetchall()
                if cr_get_avg_g.rowcount == self.rsi_period:
                    for row in result_avg_g:
                        tt_gain = tt_gain + row["gain_1d"]
                    rsi_data.c_curr_avg_gain = tt_gain / self.rsi_period
                cr_get_avg_g.close()
        else:
            #(AVG_GAIN) = ( (PREVIOUS_AVG_GAIN)*(rsi_period-1)+ (GAIN) ) / rsi_period
            rsi_data.c_curr_avg_gain = ( ( rsi_data.c_prev_avg_gain * (self.rsi_period-1) )+ rsi_data.c_curr_gain )/self.rsi_period                       
        return rsi_data.c_curr_avg_gain
    
    def get_avg_loss(self):
        #(AVG_LOSS) = ( (PREVIOUS_AVG_LOSS)*(rsi_period-1)+ (LOSS) ) / rsi_period
        tt_loss = 0
        if rsi_data.c_prev_avg_loss == 0:
            with rsi_data.connection.cursor() as cr_get_avg_l:
                sql_get_avg_l = "SELECT avg_loss, loss_1d FROM price_instruments_data "+\
                              "WHERE symbol='"+self.symbol+"' AND date<"+str(self.date)+" AND is_ta_calc=1 "+\
                              "LIMIT "+str(self.rsi_period)
                cr_get_avg_l.execute(sql_get_avg_l)
                result_avg_l = cr_get_avg_l.fetchall()
                if cr_get_avg_l.rowcount == self.rsi_period:
                    for row in result_avg_l:
                        tt_loss = tt_loss + row["loss_1d"]
                    rsi_data.c_curr_avg_loss = tt_loss / self.rsi_period
                cr_get_avg_l.close()
        else:
            #(AVG_LOSS) = ( (PREVIOUS_AVG_LOSS)*(rsi_period-1)+ (LOSS) ) / rsi_period
            rsi_data.c_curr_avg_loss = ( ( rsi_data.c_prev_avg_loss * (self.rsi_period-1) )+ rsi_data.c_curr_loss )/self.rsi_period                       
        return rsi_data.c_curr_avg_loss
    
    def get_loss(self):
        loss_1d = 0    
        if rsi_data.c_change_1d < 0:
            loss_1d = (rsi_data.c_change_1d)*(-1)
        rsi_data.c_curr_loss = loss_1d
        return loss_1d

    def get_change(self):
        rsi_data.c_change_1d = rsi_data.c_curr_price_close - rsi_data.c_prev_price_close
        return rsi_data.c_change_1d

    def get_rs(self):
        #(RS) = (AVG_GAIN) / (AVG_LOSS)
        if rsi_data.c_curr_avg_loss != 0:
            rsi_data.c_rs = rsi_data.c_curr_avg_gain / rsi_data.c_curr_avg_loss
        return rsi_data.c_rs

    def get_rsi(self):
        #(RSI) = if( (RS)=0, 100, 100-(100/1+(RS)) )
        if rsi_data.c_curr_avg_gain != 0:
            if rsi_data.c_rs == 0:
                rsi_data.c_rsi = 100
            else:
                rsi_data.c_rsi = 100-( 100 / (1+ rsi_data.c_rs) )
        return rsi_data.c_rsi

    def get_rsi_overbought(self):
        return 70

    def get_rsi_oversold(self):
        return 30
            
