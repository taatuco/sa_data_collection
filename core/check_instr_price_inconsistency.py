""" Check price that are inconsistent and send a report by email """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
from datetime import timedelta
import pymysql.cursors
from sa_numeric import get_pct_change
from sa_logging import log_this
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

def check_instr_is_obsolete(symbol, connection):
    """
    Check if a particular symbol did not get price update for more than 7 days.
    If yes, the symbol will be logged.
    Args:
        String: Instrument symbol
    Returns:
        None
    """
    k = 7
    module = '{symbol} = No data collected since more than 7 days.'
    status = 1
    date_range = datetime.datetime.now() - timedelta(days=k)
    date_range = date_range.strftime("%Y%m%d")
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT COUNT(*) FROM price_instruments_data WHERE symbol = "'+\
    symbol + '" AND date >=' + date_range
    cursor.execute(sql)
    res = cursor.fetchall()
    count_record = 0
    for row in res:
        count_record = row[0]
    if count_record == 0:
        log_this(module.replace('{symbol}', symbol), status)
    cursor.close()

def check_price_inconsist_price_move(symbol, connection):
    """
    Check if a particular symbol experienced an unexpected price movement
    greater than 40% due to error or possible stock split.
    In that case add symbol to log.
    Args:
        String: Instrument symbol
    Returns:
        None
    """
    k = 7
    module = '{symbol} = Price inconsistent or stock split'
    status = 1
    date_range = datetime.datetime.now() - timedelta(days=k)
    date_range = date_range.strftime("%Y%m%d")

    cr_c = connection.cursor(pymysql.cursors.SSCursor)
    sql_c = "SELECT AVG(price_close) FROM price_instruments_data WHERE symbol = '"+\
    symbol + "' AND date >=" + date_range
    cr_c.execute(sql_c)
    res_c = cr_c.fetchall()
    average_price = 0
    for row in res_c:
        average_price = row[0]
    sql_c = "SELECT price_close FROM price_instruments_data WHERE symbol = '"+\
    symbol +"' ORDER BY date DESC LIMIT 1"
    cr_c.execute(sql_c)
    res_c = cr_c.fetchall()
    last_price = 0
    for row in res_c:
        last_price = row[0]
    cr_c.close()
    debug(str(average_price)+ " ::: "+str(last_price))
    if average_price is not None:
        if abs(get_pct_change(average_price, last_price)) >= 0.4:
            log_this(module.replace('{symbol}', str(symbol)), status)
    else:
        log_this(module.replace('{symbol}', str(symbol)), status)
