""" Module that calls all related module that update data """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import gc
import datetime
from datetime import timedelta
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_portf_suffix
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_core()))
from ta_calc_ma import calc_ma
from ta_calc_rsi import RsiData
from ta_calc_tln import get_trend_line_data
from ta_instr_sum import get_instr_sum
from set_signals_feed import set_signals_feed
from set_widgets_feed import set_widgets_feed
from ta_gen_recomm import gen_recomm
from ta_gen_chart_data import clear_chart_table, gen_chart
from get_frc_pnl import get_forecast_pnl
from get_trades import get_trades
from get_sentiment_score import get_sentiment_score_avg

sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_update_instr_data(extended_scan, is_update_all, specific_symbol):
    """
    Main function to update all data
    Args:
        Integer: if 1 then update up to number of day
                    specified in variable extended_scanelse up to 10 days.
        Boolean: if 1 then update all data regardless flag is_ta_calc
        String: if not '' then update specific instrument (symbol)
    Returns:
        None
    """
    if extended_scan == 1:
        nd_scan = 370
    else:
        nd_scan = 10

    if specific_symbol == '':
        sql_parse_list = "SELECT symbol_list.symbol, symbol_list.uid, instruments.asset_class "+\
        "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol  "+\
        "WHERE symbol_list.symbol NOT LIKE '"+get_portf_suffix()+\
        "%' AND symbol_list.disabled = 0 ORDER BY symbol"
    else:
        sql_parse_list = "SELECT symbol_list.symbol, symbol_list.uid, instruments.asset_class "+\
        "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol  "+\
        "WHERE symbol_list.symbol = '"+ str(specific_symbol) +"' AND symbol_list.disabled = 0"

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    clear_chart_table(specific_symbol)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = sql_parse_list
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
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

        debug(str(uid) + ' - ' + str(s) + '------------------------------')
        debug(s +": "+ str(pip) +": "+ os.path.basename(__file__))
        dn = datetime.datetime.now() - timedelta(days=10)
        dn = dn.strftime("%Y%m%d")
        dh = datetime.datetime.now() - timedelta(days=7)
        dh = dh.strftime("%Y%m%d")
        d = datetime.datetime.now() - timedelta(days=nd_scan)
        d = d.strftime("%Y%m%d")
        sentiment = 0

        if is_update_all:
            sql_select_instr = "SELECT id, date FROM price_instruments_data "+\
            "WHERE (symbol='"+s+"' and date>"+d+") ORDER BY date ASC"
        else:
            sql_select_instr = "SELECT id, date FROM price_instruments_data "+\
            "WHERE (symbol='"+s+"' and date>"+d+" and is_ta_calc=0) ORDER BY date ASC"

        cr_d_id = connection.cursor(pymysql.cursors.SSCursor)
        sql_d_id = sql_select_instr
        cr_d_id.execute(sql_d_id)
        rs_d = cr_d_id.fetchall()
        for row in rs_d:
            d = str(row[1]).replace("-", "")
            record_id = row[0]
            rsi = RsiData(s, d, 14)
            change_1d = rsi.get_change()
            gain_1d = rsi.get_gain()
            loss_1d = rsi.get_loss()
            avg_gain = rsi.get_avg_gain()
            avg_loss = rsi.get_avg_loss()
            rs14 = rsi.get_rs()
            rsi14 = rsi.get_rsi()
            rsi_overbought = rsi.get_rsi_overbought()
            rsi_oversold = rsi.get_rsi_oversold()
            ma200 = calc_ma(s, d, 200)
            ma10 = calc_ma(s, d, 10)
            ma20 = calc_ma(s, d, 20)
            ma30 = calc_ma(s, d, 30)
            ma40 = calc_ma(s, d, 40)
            ma50 = calc_ma(s, d, 50)
            sentiment = get_sentiment_score_avg(s, dh)
            is_ta_calc = "1"
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
            "sentiment_1d="+str(sentiment)+", "+\
            "is_ta_calc="+str(is_ta_calc)+" "+\
            "WHERE id="+str(record_id)
            debug(sql_upd)
            cr_upd.execute(sql_upd)
            connection.commit()
            gc.collect()
            cr_upd.close()
        cr_d_id.close()
        gc.collect()

        if is_update_all:
            get_trades(s, uid, nd_scan, True)
        else:
            get_trades(s, uid, nd_scan, False)

        if extended_scan == 1:
            get_trend_line_data(s, uid)
            gen_recomm(s, uid)
            gen_chart(s, uid)
        get_forecast_pnl(s, nd_scan, is_update_all)
        get_instr_sum(s, uid, asset_class, dn, sentiment)
        set_signals_feed(s)
        set_widgets_feed(s)
    cursor.close()
    connection.close()
