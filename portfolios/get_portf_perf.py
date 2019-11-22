""" Get strategy portfolio performance """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
from datetime import timedelta
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_portf_suffix
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()
sys.path.append(os.path.abspath(SETT.get_path_feed()))
sys.path.append(os.path.abspath(SETT.get_path_core()))
from get_instr_perf_summ import InstrumentSummaryData
from sa_numeric import get_stdev, get_mdd, get_romad, get_volatility_risk

def get_portf_perf_summ(symbol, uid):
    """
    Get and calculate strategy portfolio performance summary
    Args:
        String: Symbol of the strategy portfolio
        Int: uid of the strategy portfolio
    Returns:
        None
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    pps = InstrumentSummaryData(symbol, uid, connection)
    y1_pct = pps.get_pct_1_year_performance()
    m6_pct = pps.get_pct_6_month_performance()
    m3_pct = pps.get_pct_3_month_performance()
    m1_pct = pps.get_pct_1_month_performance()
    w1_pct = pps.get_pct_1_week_performance()
    date_last_month = datetime.datetime.now() - timedelta(days=30)
    date_last_month = date_last_month.strftime('%Y%m%d')
    sql = "SELECT price_close FROM chart_data WHERE uid="+ str(uid) +\
    " AND date >="+ str(date_last_month) +" ORDER BY date"
    stdev_st = get_stdev(sql)
    maximum_dd_st = get_mdd(sql)
    romad_st = get_romad(sql)
    volatility_risk_st = get_volatility_risk(sql, True, symbol)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "UPDATE instruments SET y1="+ str(y1_pct) +", m6="+ str(m6_pct) +", m3="+\
    str(m3_pct) +", m1="+ str(m1_pct) +", w1="+ str(w1_pct) +", "+\
    " stdev_st="+ str(stdev_st) + ", maximum_dd_st="+ str(maximum_dd_st) +\
    ", romad_st="+ str(romad_st) + ", volatility_risk_st="+ str(volatility_risk_st) +\
    " WHERE symbol='"+ str(symbol)  +"' "
    debug(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

def get_portf_pnl(portf_symbol, date_last_year_str):
    """
    Get strategy portfolio profit and loss according to args.
    Args:
        String: Symbol of the strategy portfolio
        String: date from last year in string format
    Returns:
        Double: Strategy portfolio profit and loss
    """
    ret = 0
    portf_pnl = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT price_instruments_data.pnl, portfolios.quantity, "+\
    "instruments.pip, "+\
    "price_instruments_data.pnl_long, price_instruments_data.pnl_short, "+\
    "portfolios.strategy_order_type " +\
    "FROM portfolios JOIN price_instruments_data ON "+\
    "portfolios.symbol = price_instruments_data.symbol "+\
    "JOIN instruments ON portfolios.symbol = instruments.symbol "+\
    "WHERE portfolios.portf_symbol = '"+ portf_symbol +"' AND date="+\
    date_last_year_str +" ORDER BY portfolios.portf_symbol"
    debug(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        pnl_c = row[0]
        quantity_c = row[1]
        pip_c = row[2]
        pnl_long_c = row[3]
        pnl_short_c = row[4]
        strategy_order_type_c = row[5]
        if strategy_order_type_c == 'long/short':
            portf_pnl = portf_pnl + (pnl_c * quantity_c * pip_c)
        if strategy_order_type_c == 'long' and pnl_long_c != 999:
            portf_pnl = portf_pnl + (pnl_long_c * quantity_c * pip_c)
        if strategy_order_type_c == 'short' and pnl_short_c != 999:
            portf_pnl = portf_pnl + (pnl_short_c * quantity_c * pip_c)
    ret = portf_pnl
    cursor.close()
    connection.close()
    return ret

def get_portf_perf():
    """
    Description
    Args:
        None
    Returns:
        None
    """
    portf_symbol_suffix = get_portf_suffix()
    day_last_year = datetime.datetime.now() - timedelta(days=370)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.symbol, symbol_list.uid, instruments.fullname, "+\
    "instruments.account_reference "+\
    "FROM `symbol_list` INNER JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.symbol LIKE '"+portf_symbol_suffix+"%' ORDER BY symbol_list.symbol"
    cursor.execute(sql)
    res = cursor.fetchall()

    for row in res:
        portf_symbol = row[0]
        portf_uid = row[1]
        account_reference = row[3]

        i = 0
        j = 370
        date_last_year = day_last_year
        inserted_value = ''
        portf_nav = account_reference

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM chart_data WHERE uid = "+ str(portf_uid)
        debug(sql_i)
        cr_i.execute(sql_i)
        connection.commit()
        cr_i.close()

        while i <= j:

            date_last_year = date_last_year + timedelta(days=1)
            date_last_year_str = date_last_year.strftime("%Y%m%d")
            portf_pnl = 0

            #get portfolio allocations
            #for each item get the pnl
            if date_last_year < datetime.datetime.now():
                portf_pnl = get_portf_pnl(portf_symbol, date_last_year_str)
                portf_nav = round(portf_nav + portf_pnl, 2)

                if i > 0:
                    sep = ', '
                else:
                    sep = ''
                inserted_value = inserted_value + sep + "(" + str(portf_uid) +\
                ",'"+ str(portf_symbol) +"','" + str(date_last_year_str) + "'," +\
                str(portf_nav) + ")"
            i += 1

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "INSERT IGNORE INTO chart_data(uid, symbol, date, price_close) VALUES "+\
        inserted_value
        debug(sql_i)
        cr_i.execute(sql_i)
        connection.commit()
        cr_i.close()
        get_portf_perf_summ(portf_symbol, portf_uid)
    cursor.close()
    connection.close()
