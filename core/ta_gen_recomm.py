""" Functionalities related to recommendations text """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import csv
from pathlib import Path
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()

sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def get_rsi_mom(oversold, overbought, weak, strong, lt_rsi_mom):
    """
    Get relative strength index momentum
    Args:
        String: Oversold text
        String: Overbought text
        String: Weak text
        String: Long term rsi text signal
    Returns:
        String: rsi momentum text
    """
    ret = ''
    if lt_rsi_mom.lower() == 'overbought':
        ret = overbought
    if lt_rsi_mom.lower() == 'oversold':
        ret = oversold
    if lt_rsi_mom.lower() == 'weak':
        ret = weak
    if lt_rsi_mom.lower() == 'strong':
        ret = strong
    return ret

def gen_recomm(symbol, uid):
    """
    Update recommendations, modify record in table recommendations
    Args:
        String: Instrument symbol
        Integer: Instrument unique id
    Returns:
        None
    """
    week_forecast = 0
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

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT decimal_places, fullname FROM instruments WHERE symbol='"+str(symbol)+"'"
    debug(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        decimal_places = int(row[0])
        instr_fullname = row[1]


    sql = "SELECT trade_1_entry, trade_1_tp, trade_1_sl, trade_1_type, "+\
    "trade_3_entry, trade_3_tp, trade_3_sl, trade_3_type, wf "+\
    "FROM instruments WHERE symbol ='" + str(symbol) + "'"
    debug(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        trade_1_entry = row[0]
        trade_1_tp = row[1]
        trade_1_sl = row[2]
        trade_1_type = row[3]
        trade_3_entry = row[4]
        trade_3_tp = row[5]
        trade_3_sl = row[6]
        trade_3_type = row[7]
        week_forecast = row[8]

        if trade_1_type == 'buy':
            buy_entry = round(trade_1_entry, decimal_places)
            buy_tp = round(trade_1_tp, decimal_places)
            buy_sl = round(trade_1_sl, decimal_places)

        if trade_3_type == 'sell':
            sell_entry = round(trade_3_entry, decimal_places)
            sell_tp = round(trade_3_tp, decimal_places)
            sell_sl = round(trade_3_sl, decimal_places)
    cursor.close()

    data_src = SETT.get_path_src()
    file_this = data_src+str(uid)+'t.csv'
    filepath = Path(file_this)
    if filepath.exists():
        with open(file_this) as csvfile:
            csv_file = csv.reader(csvfile, delimiter=',')
            i = 1
            for row in csv_file:
                if i == 2:
                    ma200 = round(float(row[18]), decimal_places)
                    st_upper_range = round(float(row[11]), decimal_places)
                    st_lower_range = round(float(row[10]), decimal_places)
                    lt_rsi_avg = round(float(row[14]), decimal_places)
                    lt_rsi_mom = row[17]
                i += 1

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT price_close FROM price_instruments_data WHERE symbol='"+\
    str(symbol)+"' ORDER BY date DESC LIMIT 1"
    debug(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        last_price = row[0]
    cursor.close()

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT * FROM recommendations"
    debug(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
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

        if last_price < ma200:
            pt1 = price_under_200ma
        if last_price > ma200:
            pt1 = price_above_200ma
        if st_upper_range > last_price:
            pt2 = st_upper_range_above_price_range
        if st_lower_range < last_price:
            pt2 = st_lower_range_below_price_range
        if st_upper_range < last_price and week_forecast < 0:
            pt3 = upper_range_below_price_downtrend
        if st_lower_range > last_price and week_forecast >= 0:
            pt3 = lower_range_above_price_uptrend
        pt4 = get_rsi_mom(rsi_oversold, rsi_overbought, rsi_weak, rsi_strong, lt_rsi_mom)
        if week_forecast < 0:
            pt5 = downtrend_recomm
        else:
            pt5 = uptrend_recomm

        pt1 = pt1.replace("{symbol}", instr_fullname)
        pt2 = pt2.replace("{st_upper_range}", str(st_upper_range))
        pt2 = pt2.replace("{st_lower_range}", str(st_lower_range))
        pt3 = pt3.replace("{symbol}", instr_fullname)
        pt3 = pt3.replace("{st_upper_range}", str(st_upper_range))
        pt3 = pt3.replace("{st_lower_range}", str(st_lower_range))
        pt4 = pt4.replace("{symbol}", instr_fullname)
        pt4 = pt4.replace("{rsi_50_day_avg}", str(round(float(lt_rsi_avg), 2)))
        pt5 = pt5.replace("{symbol}", instr_fullname)
        pt5 = pt5.replace("{buy_entry}", str(buy_entry))
        pt5 = pt5.replace("{buy_target_price}", str(buy_tp))
        pt5 = pt5.replace("{buy_stop_loss}", str(buy_sl))
        pt5 = pt5.replace("{sell_entry}", str(sell_entry))
        pt5 = pt5.replace("{sell_target_price}", str(sell_tp))
        pt5 = pt5.replace("{sell_stop_loss}", str(sell_sl))


        result = pt1 + " " + pt2 + " " + pt3 + " " + pt4 + " " + pt5

        if result != '':
            cr_u = connection.cursor(pymysql.cursors.SSCursor)
            sql_u = "UPDATE instruments SET recommendation='"+\
            str(result) +"' WHERE symbol='" + str(symbol) + "'"
            debug(sql)
            cr_u.execute(sql_u)
            connection.commit()
            cr_u.close()
    cursor.close()

    debug(str(uid) +": "+ os.path.basename(__file__))
