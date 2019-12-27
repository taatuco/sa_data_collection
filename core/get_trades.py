""" Generate trades from signals that are stored in price_instruments_data """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
from datetime import timedelta, date
import pymysql.cursors
from sa_numeric import get_pct_change
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

def get_trades(symbol, uid, number_of_days, full_update, connection):
    """
    Generate trades from price_instruments_data
    Args:
        String: Symbol of the selected instrument
        Integer: Uid of the selected instrument
        Integer: Number of days / trades
        Boolean: If True, the entire list of trades is rebuilt
    Returns:
        None
    """
    daycount = number_of_days + 10
    dfrom = datetime.datetime.now() - timedelta(days=daycount)
    dfrom_str = dfrom.strftime('%Y%m%d')
    date_today = date.today()

    trade_symbol = symbol
    trade_fullname = ''
    trade_order_type = ''
    trade_entry_price = ''
    trade_entry_date = dfrom
    trade_expiration_date = dfrom
    trade_close_price = -1
    trade_pnl_pct = 0
    trade_status = ''
    trade_last_price = 0
    trade_decimal_places = 0
    trade_url = "s/?uid="+ str(uid)

    if full_update:
        sql_delete_trades = "DELETE FROM trades WHERE symbol = '"+ symbol +"' "
    else:
        sql_delete_trades = "DELETE FROM trades WHERE symbol ='"+ symbol +"' AND status='active' "

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = sql_delete_trades
    cursor.execute(sql)
    connection.commit()

    sql = "SELECT decimal_places, fullname FROM instruments WHERE symbol = '"+\
    symbol +"' "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        trade_decimal_places = row[0]
        trade_fullname = row[1].replace("'", "`")

    sql = "SELECT price_close FROM price_instruments_data WHERE symbol = '"+ symbol +\
    "' ORDER BY date DESC LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        trade_last_price = row[0]
    cursor.close()

    cr_1 = connection.cursor(pymysql.cursors.SSCursor)
    sql_1 = "SELECT symbol, date, price_close, target_price "+\
    "FROM price_instruments_data WHERE symbol = '"+ symbol +"' AND date >=" +\
    dfrom_str + " ORDER BY date"
    cr_1.execute(sql_1)
    rs_1 = cr_1.fetchall()
    i = 0
    inserted_value = ''
    for row in rs_1:
        date_1 = row[1]
        price_close_1 = round(row[2], trade_decimal_places)
        target_price_1 = round(row[3], trade_decimal_places)

        dto = date_1 + timedelta(days=8)
        dto_str = dto.strftime('%Y%m%d')
        cr_2 = connection.cursor(pymysql.cursors.SSCursor)
        sql_2 = "SELECT date, price_close FROM price_instruments_data WHERE symbol = '"+\
        symbol +"' AND date >=" + dto_str + " ORDER BY date LIMIT 1"
        debug(sql_2)
        cr_2.execute(sql_2)
        rs_2 = cr_2.fetchall()
        date_2 = None
        price_close_2 = -1
        for row in rs_2:
            date_2 = row[0]
            price_close_2 = round(row[1], trade_decimal_places)
        cr_2.close()

        if target_price_1 != -9:
            if price_close_1 <= target_price_1:
                trade_order_type = 'buy'
            if price_close_1 > target_price_1:
                trade_order_type = 'sell'

        debug(str(date_1) + " ::: " + str(price_close_1) + " ::: " +\
              str(target_price_1) + " ::: " + str(trade_order_type))

        trade_entry_price = price_close_1
        trade_entry_date = date_1 + timedelta(days=1)
        if date_2 is not None:
            trade_expiration_date = date_2
        else:
            trade_expiration_date = date_1 + timedelta(days=8)
        trade_close_price = price_close_2
        if price_close_2 == -1:
            trade_status = 'active'
            if trade_order_type == 'buy':
                trade_pnl_pct = get_pct_change(price_close_1, trade_last_price)
            else:
                trade_pnl_pct = get_pct_change(trade_last_price, price_close_1)

        else:
            trade_status = 'expired'
            if trade_order_type == 'buy':
                trade_pnl_pct = get_pct_change(price_close_1, price_close_2)
            else:
                trade_pnl_pct = get_pct_change(price_close_2, price_close_1)

        if i == 0:
            sep = ''
        else:
            sep = ','

        if target_price_1 != -9:
            if trade_entry_date <= date_today:
                inserted_value = inserted_value + sep + "("+  str(uid)  +", '"+\
                trade_symbol +"', '"+\
                trade_fullname  +"', '" + trade_order_type +"',"+ str(trade_entry_price) +\
                ",'"+ str(trade_entry_date) +"','"+\
                str(trade_expiration_date) +"',"+ str(trade_close_price) +","+\
                str(trade_pnl_pct) +\
                ",'"+ str(trade_status) +"', '"+ str(trade_url) + "' " +")"
                i += 1
    cr_1.close()
    if inserted_value != '':
        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "INSERT IGNORE INTO trades(uid, symbol, fullname, order_type, entry_price, "+\
        "entry_date, expiration_date, close_price, pnl_pct, status, url) VALUES "+ inserted_value
        debug(sql_i)
        cr_i.execute(sql_i)
        connection.commit()
        cr_i.close()
