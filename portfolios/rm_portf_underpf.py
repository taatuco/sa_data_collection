""" Evaluate and remove underperforming strategy portfolios (auto-generated) """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import gc
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, get_portf_suffix, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def rm_portf_underpf(limit_max):
    """
    Remove underperforming strategy portfolio that are auto-generated.
    Auto-generated portfolio strategy are used as example.
    Args:
        Int: Maximum number of example to keep.
    Returns:
        None
    """
    total = 0
    quant_to_rm = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT COUNT(*) FROM instruments JOIN users ON instruments.owner = users.id'
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        total = row[0]
    quant_to_rm = int(total) - int(limit_max)


    if quant_to_rm > 0:
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT instruments.symbol, users.is_bot '+\
        'FROM instruments JOIN users ON instruments.owner = users.id '+\
        'WHERE users.is_bot=1 AND instruments.symbol LIKE "%'+\
        get_portf_suffix() +'%" ORDER BY instruments.y1 '+\
        'LIMIT '+ str(quant_to_rm)
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            symbol = row[0]
            rm_portf_from('feed', 'symbol', symbol)
            rm_portf_from('chart_data', 'symbol', symbol)
            rm_portf_from('portfolios', 'portf_symbol', symbol)
            rm_portf_from('instruments', 'symbol', symbol)
            rm_portf_from('symbol_list', 'symbol', symbol)
    cursor.close()
    connection.close()

def rm_portf_from(table, column, symbol):
    """
    Remove strategy portfolio from table as per args
    Args:
        String: Name of the table
        String: Column used for filtering
        String: Symbol of the strategy portfolio
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
    sql = 'DELETE FROM '+ str(table) +' WHERE '+ column +' = "'+ str(symbol) +'"'
    debug(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    gc.collect()
