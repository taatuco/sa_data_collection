# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import gc
import time
import datetime
from datetime import timedelta

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

sys.path.append(os.path.abspath( sett.get_path_core() ))
from ta_calc_ma import *
from ta_calc_rsi import *
from ta_calc_tln import *
from ta_instr_sum import *
from ta_calc_up_dn_stats import *
from set_signals_feed import *
from ta_gen_recomm import *
from ta_gen_chart_data import *
from get_frc_pnl import *
from get_trades import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_update_instr_data(fm,is_update_all):

    if fm == 1:
        nd_scan = 370
    else:
        nd_scan = 10

    specific_symbol = sys.argv[1]

    if specific_symbol == None:
        sql_parse_list = "SELECT symbol_list.symbol, symbol_list.uid, instruments.asset_class "+\
        "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol  WHERE symbol_list.symbol NOT LIKE '"+get_portf_suffix()+"%' ORDER BY symbol"
    else:
        sql_parse_list = "SELECT symbol_list.symbol, symbol_list.uid, instruments.asset_class "+\
        "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol  WHERE symbol_list.symbol = '"+ str(specific_symbol) +"'"

    import pymysql.cursors
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = sql_parse_list
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            s = row[0]
            uid = row[1]
            asset_class = row[2]
            cr_pip = connection.cursor(pymysql.cursors.SSCursor)
            sql_pip = "SELECT pip FROM instruments WHERE symbol ='"+ s +"' "
            cr_pip.execute(sql_pip)
            rs_pip = cr_pip.fetchall()
            for row in rs_pip:
                pip = row[0]
            cr_pip.close()

            print(s +": "+ str(pip) +": "+ os.path.basename(__file__) )
            dn = datetime.datetime.now() - timedelta(days=10)
            dn = dn.strftime("%Y%m%d")
            d = datetime.datetime.now() - timedelta(days=nd_scan)
            d = d.strftime("%Y%m%d")

            if is_update_all:
                sql_select_instr = "SELECT id, date FROM price_instruments_data WHERE (symbol='"+s+"' and date>"+d+") ORDER BY date ASC"
            else:
                sql_select_instr = "SELECT id, date FROM price_instruments_data WHERE (symbol='"+s+"' and date>"+d+" and is_ta_calc=0) ORDER BY date ASC"

            cr_d_id = connection.cursor(pymysql.cursors.SSCursor)
            sql_d_id = sql_select_instr
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
                ma10 = calc_ma(s,d,10)
                ma20 = calc_ma(s,d,20)
                ma30 = calc_ma(s,d,30)
                ma40 = calc_ma(s,d,40)
                ma50 = calc_ma(s,d,50)

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
                    "ma10="+str(ma10)+ ", "+\
                    "ma20="+str(ma20)+ ", "+\
                    "ma30="+str(ma30)+ ", "+\
                    "ma40="+str(ma40)+ ", "+\
                    "ma50="+str(ma50)+ ", "+\
                    "is_ta_calc="+str(is_ta_calc)+" "+\
                    "WHERE id="+str(id)
                    cr_upd.execute(sql_upd)
                    connection.commit()
                    cr_upd.close()
                    print(sql_upd)
                except:
                    sql_upd = "UPDATE price_instruments_data SET "+\
                    "is_ta_calc=1 "+\
                    "WHERE id="+str(id)
                    cr_upd.execute(sql_upd)
                    connection.commit()
                    cr_upd.close()

            cr_d_id.close()
            gc.collect()
            if fm == 1:
                get_trend_line_data(s,uid)
                get_day_up_dwn_stat(s,uid)
                set_signals_feed(s)
                gen_recomm(s,uid)
                gen_chart(s,uid)
            get_forecast_pnl(s,uid,nd_scan)
            get_trades(s,uid,nd_scan)
            get_instr_sum(s,uid,asset_class,dn,pip)
            set_signals_feed(s)

        cr.close()

    finally:
        connection.close()
