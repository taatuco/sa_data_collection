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
from set_signals_feed import *
from set_widgets_feed import *
from ta_gen_recomm import *
from ta_gen_chart_data import *
from get_frc_pnl import *
from get_trades import *
from get_sentiment_score import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_update_instr_data(fm,is_update_all,specific_symbol):

    if fm == 1:
        nd_scan = 370
    else:
        nd_scan = 10

    if specific_symbol == None or specific_symbol == '':
        sql_parse_list = "SELECT symbol_list.symbol, symbol_list.uid, instruments.asset_class "+\
        "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol  WHERE symbol_list.symbol NOT LIKE '"+get_portf_suffix()+"%' AND symbol_list.disabled = 0 ORDER BY symbol"
    else:
        sql_parse_list = "SELECT symbol_list.symbol, symbol_list.uid, instruments.asset_class "+\
        "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol  WHERE symbol_list.symbol = '"+ str(specific_symbol) +"' AND symbol_list.disabled = 0"

    import pymysql.cursors
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        clear_chart_table(specific_symbol)

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

            print(str(uid) + ' - ' + str(s) + '------------------------------' )
            print(s +": "+ str(pip) +": "+ os.path.basename(__file__) )
            dn = datetime.datetime.now() - timedelta(days=10)
            dn = dn.strftime("%Y%m%d")
            dh = datetime.datetime.now() - timedelta(days=7)
            dh = dh.strftime("%Y%m%d")

            d = datetime.datetime.now() - timedelta(days=nd_scan)
            d = d.strftime("%Y%m%d")

            sentiment = 0

            if is_update_all:
                sql_select_instr = "SELECT id, date FROM price_instruments_data WHERE (symbol='"+s+"' and date>"+d+") ORDER BY date ASC"
            else:
                sql_select_instr = "SELECT id, date FROM price_instruments_data WHERE (symbol='"+s+"' and date>"+d+" and is_ta_calc=0) ORDER BY date ASC"

            cr_d_id = connection.cursor(pymysql.cursors.SSCursor)
            sql_d_id = sql_select_instr
            cr_d_id.execute(sql_d_id)
            rs_d = cr_d_id.fetchall()
            case_block = ''
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
                sentiment = get_sentiment_score_avg(s,dh)
                is_ta_calc = "1"

                try:
                    case_block = case_block +\
                    "change_1d= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(change_1d)+ " END, "+\
                    "gain_1d= CASE"+\
                    "   WHEN id="+str(id)+" THEN "+str(gain_1d)+" END, "+\
                    "loss_1d= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(loss_1d)+" END, "+\
                    "avg_gain= CASE"+\
                    "   WHEN id="+str(id)+" THEN "+str(avg_gain)+" END, "+\
                    "avg_loss= CASE"+\
                    "   WHEN id="+str(id)+" THEN "+str(avg_loss)+" END, "+\
                    "rs14= CASE"+\
                    "   WHEN id="+str(id)+" THEN "+str(rs14)+" END, "+\
                    "rsi14= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(rsi14)+" END, "+\
                    "rsi_overbought= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(rsi_overbought)+" END, "+\
                    "rsi_oversold= CASE"+\
                    "   WHEN id="+str(id)+" THEN "+str(rsi_oversold)+" END, "+\
                    "ma200= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(ma200)+ " END, "+\
                    "ma10= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(ma10)+ " END, "+\
                    "ma20= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(ma20)+ " END, "+\
                    "ma30= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(ma30)+ " END, "+\
                    "ma40= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(ma40)+ " END, "+\
                    "ma50= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(ma50)+ " END, "+\
                    "sentiment_1d= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(sentiment)+" END, "+\
                    "is_ta_calc= CASE "+\
                    "   WHEN id="+str(id)+" THEN "+str(is_ta_calc)+"END, "
                except:
                    case_block = case_block +\
                    'is_ta_calc = CASE '+\
                    '   WHEN id='+ str(id)+' THEN 1'+\
                    'END, '
            try:
                cr_upd = connection.cursor(pymysql.cursors.SSCursor)
                sql_upd = 'UPDATE price_instruments_data SET ' + case_block
                print(sql_upd)
                cr.upd_execute(sql_upd)
                connection.commit()
            except:
                sql_upd = 'UPDATE price_instruments_data SET ' + case_block
                print(sql_upd)
                cr.upd_execute(sql_upd)
                connection.commit()


            cr_d_id.close()
            gc.collect()

            if is_update_all:
                get_trades(s,uid,nd_scan,True)
            else:
                get_trades(s,uid,nd_scan,False)

            if fm == 1:
                get_trend_line_data(s,uid)
                gen_recomm(s,uid)
                gen_chart(s,uid)
            get_forecast_pnl(s,uid,nd_scan,is_update_all)

            get_instr_sum(s,uid,asset_class,dn,pip,sentiment)
            set_signals_feed(s)
            set_widgets_feed(s)

        cr.close()

    finally:
        connection.close()
