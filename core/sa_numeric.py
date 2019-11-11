""" All numerical functionalities """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import math
import numpy as np
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


def get_pct_change(ini_val, new_val):
    """
    Get percentage change between two values
    Args:
        Double: Initial value
        Double: New value
    Returns:
        Double: Percentage change between the 2 values
    """
    if not new_val == 0:
        if new_val < ini_val:
            ret = ((ini_val - new_val) / ini_val) * (-1)
        else:
            ret = (new_val - ini_val) / new_val
    else:
        ret = 0

    return ret


def get_stdev(sql):
    """
    sql with just one numerical value to compute standard deviation
    Compute standard deviation from a database table column.
    Args:
        String: SQL query with only 1 numerical column
    Returns:
        Double: Standard deviation
    """
    ret = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    std_is = list(cursor.fetchall())
    ret = np.std(std_is)
    debug('stdev='+str(ret))
    cursor.close()
    connection.close()
    if ret is None:
        ret = 0
    return ret

def get_volatility_risk(sql, is_portf, symbol):
    """
    Get the volatility risk of an instrument, or strategy portfolio.
    Args:
        String: SQL query with one column corresponding to close_price
        Boolean: If True, calculation of a strategy portfolio. False = instrument
        String: Symbol of instrument or strategy portfolio
    Returns:
        Double: volatility risk in percentage.
    """
    ret = 0
    #sql with one numerical column to compute volatility risk
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    if is_portf:
        sql_i = "SELECT account_reference FROM instruments WHERE symbol='"+ symbol +"'"
        cursor.execute(sql_i)
        res = cursor.fetchall()
        for row in res:
            last_price = row[0]
        cursor.close()
    else:
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            last_price = row[0]
        cursor.close()
        connection.close()
    stdev = get_stdev(sql)
    price_minus_stdev = last_price - stdev
    ret = abs(get_pct_change(last_price, price_minus_stdev))
    return ret

def get_mdd(sql):
    """
    Get maximum drawdown from a list of price
    Args:
        String: SQL query with one column containing price
    Returns:
        Double: Return the maximum drawdown in percentage
    """
    ret = 0
    #sql with just one numerical value to compute maximum drawdown
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    top = 0
    breset = math.pow(10, 100)
    bottom = breset
    pct_dd = 0
    cur_dd = 0
    for row in res:
        val = row[0]

        if val > top:
            top = val
            bottom = breset

        if val < bottom:
            bottom = val

        if bottom < top:
            cur_dd = abs(get_pct_change(bottom, top))
        else:
            cur_dd = 0

        if cur_dd > pct_dd:
            pct_dd = cur_dd
    cursor.close()
    connection.close()
    ret = pct_dd
    debug('mdd='+ str(ret))
    return ret

def get_romad(sql):
    """
    Get return over max drawdown
    Args:
        String: SQL query with one column containing price.
    Returns:
        Double: Return RoMaD
    """
    ret = 0
    #sql with one column as numerical value to compute return on maximum drawdown
    #ordered by date ASC
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    first = 0
    last = 0
    for row in res:
        if i == 0:
            first = row[0]
        last = row[0]
        i += 1
    cursor.close()
    connection.close()

    debug('f='+str(first) + ' l='+str(last))

    percent_return = get_pct_change(first, last)
    max_drawdown = get_mdd(sql)

    ret = percent_return / max_drawdown
    debug('romad='+ str(ret))
    return ret
