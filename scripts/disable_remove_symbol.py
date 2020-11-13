""" Disable or remove a symbol. Flag disabled in Symbol_list table """
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


def disable_symbol(symbol):
    """
    disable symbol in table symbol_list
    Args:
        String: symbol
    Returns:
        None
    """
    update_s_table(symbol)


def update_s_table(symbol):
    """
    Perform update according to args. disable symbol accordingly.
    Args:
        String: symbol
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
    sql = 'UPDATE symbol_list SET symbol_list.disabled=1 ' +\
    'WHERE symbol="'+ str(symbol) +'"'
    print(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


print("###############################################################################")
print("Disable or remove a symbol function")
print("--------------------------------------")
print("IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT")
print("disable_symbol(symbol)")
print(" ")
print("provide the following parameters:")
print("(1) symbol/ticker")
print("--------------------------------------")
print("Affected tables/column:")
print("-----------------------")
print("1. symbol_list.symbol")
print("###############################################################################")
