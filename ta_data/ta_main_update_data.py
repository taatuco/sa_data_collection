# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import gc
import time

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

sys.path.append(os.path.abspath( sett.get_path_data() ))
from ta_calc_ma import *
from ta_calc_rsi import *
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
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol, r_quantmod FROM symbol_list ORDER BY symbol"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        symbol_quantmod = row[1]
        s = row[0]
        print(s + ": "+ os.path.basename(__file__) )

        cr_d_id = connection.cursor(pymysql.cursors.SSCursor)
        sql_d_id = "SELECT id, date FROM price_instruments_data "+\
        "WHERE symbol='"+s+"' and is_ta_calc=0 ORDER BY date ASC"
        cr_d_id.execute(sql_d_id)
        rs_d = cr_d_id.fetchall()
        for row in rs_d:
            d = str(row[1]).replace("-","")
            id = row[0]
            rsi = rsi_data(s,d,14)
            change_1d = rsi.get_change()
            gain_1d = rsi.get_gain()
            loss_1d = rsi.get_loss()
            avg_gain = rsi.get_avg_gain()
            avg_loss = rsi.get_avg_loss()
            rs14 = rsi.get_rs()
            rsi14 = rsi.get_rsi()
            rsi_overbought = rsi.get_rsi_overbought()
            rsi_oversold = rsi.get_rsi_oversold()
            ma200 = calc_ma(s,d,200)
            is_ta_calc = "1"

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
        gc.collect()
        time.sleep(0.2)
        cr_d_id.close()
        # Calc other data as per symbol
        get_trend_line_data(s)

    cr.close()

finally:
    connection.close()
