""" Update all involved records in database while symbol is renamed """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def rename_symbol(current_symbol, new_symbol):
    """
    Rename symbol in all involved tables of the database
    Args:
        String: Provide the original symbol
        String: Provide the new symbol
    Returns:
        None
    """
    rename_s_table('symbol_list', current_symbol, new_symbol)
    rename_s_table('instruments', current_symbol, new_symbol)
    rename_s_table('feed', current_symbol, new_symbol)
    rename_s_table('trades', current_symbol, new_symbol)
    rename_s_table('chart_data', current_symbol, new_symbol)
    rename_s_table('portfolios', current_symbol, new_symbol)
    rename_s_table('price_instruments_data', current_symbol, new_symbol)

def rename_s_table(table, current_s, new_s):
    """
    Perform update according to args. Rename symbol accordingly.
    Args:
        String: Table to update
        String: Current symbol
        String: New symbol to update to
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
    sql = 'UPDATE '+ str(table) + ' SET symbol="'+ str(new_s) +\
    '" WHERE symbol="'+ str(current_s) +'"'
    print(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


print("###############################################################################")
print("Rename symbol function")
print("--------------------------------------")
print("IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT")
print("rename_symbol(current_symbol,new_symbol)")
print(" ")
print("provide the following parameters:")
print("(1) the current symbol")
print("(2) the new symbol to change to...")
print("--------------------------------------")
print("Affected tables/column:")
print("-----------------------")
print("1. symbol_list.symbol")
print("2. instruments.symbol")
print("3. feed.symbol")
print("4. trades.symbol")
print("5. chart_data.symbol")
print("6. portfolios.symbol")
print("7. price_instruments_data.symbol")
print("###############################################################################")
