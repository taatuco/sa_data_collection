""" Manage stock split update historical price to match new price after split """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
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
sys.path.append(os.path.abspath(SETT.get_path_core()))
from ta_main_update_data import get_update_instr_data


def correct_stock_split_price(symbol, to_this_date_included, split_factor):
    """
    Correction of the historical prices according to stock split.
    Args:
        String: Provide symbol of the instrument to update
        Int: Change historical price up to this date included. (yyyymmdd)
        Double: Split multiplier.
    Returns:
        None
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT date, price_close, target_price, ma200, ma10, ma20, ma30, '+\
    'ma40, ma50 FROM price_instruments_data WHERE symbol = "'+\
    symbol +'" AND date <= '+ str(to_this_date_included) +' '
    cursor.execute(sql)
    res = cursor.fetchall()
    sql_update = ''
    for row in res:
        this_date = row[0]
        price_close = row[1]
        target_price = row[2]
        ma200 = row[3]
        ma10 = row[4]
        ma20 = row[5]
        ma30 = row[6]
        ma40 = row[7]
        ma50 = row[8]
        new_price_close = price_close * split_factor
        new_target_price = target_price * split_factor
        new_ma200 = ma200 * split_factor
        new_ma10 = ma10 * split_factor
        new_ma20 = ma20 * split_factor
        new_ma30 = ma30 * split_factor
        new_ma40 = ma40 * split_factor
        new_ma50 = ma50 * split_factor
        sql_update = 'UPDATE price_instruments_data SET price_close = ' +\
        str(new_price_close) + ', target_price = ' + str(new_target_price) +\
        ', ma200 = ' + str(new_ma200) + ', ma10 = ' + str(new_ma10) + ', ma20 = ' +\
        str(new_ma20) + ', ma30 = ' + str(new_ma30) + ', ma40 = ' + str(new_ma40) +\
        ', ma50 = ' + str(new_ma50) + ' ' +\
        'WHERE symbol = "'+ symbol +'" AND date = ' + str(this_date.strftime('%Y%m%d'))
        debug(sql_update)
        cursor.execute(sql_update)
        connection.commit()

    get_update_instr_data(1, True, symbol)

    cursor.close()
    connection.close()

    debug('Done!')


print("###############################################################################")
print("Stock split and reverse split function")
print("--------------------------------------")
print("IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT")
print("correct_stock_split_price(symbol,to_this_date_included, split_factor)")
print(" ")
print("provide the following parameters:")
print("(1) symbol")
print("(2) date until the split day (included). ie: 20190410 (for April 10, 2019)")
print("(3) multiplier. ie: reverse split: 1/4 split = then it is 4")
print("(3) multiplier. ie: split: 4 split = then it is 0.25")
print("(3) multiplier. ie: price before was $2 then new price is $14 then multiplier will be 7")
print("(3) multiplier. ie: price before was $10 then new price is $5 then multiplier will be 0.5")
print("###############################################################################")
