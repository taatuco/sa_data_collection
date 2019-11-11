""" Recalculate historical data for a specific instrument """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import pymysql.cursors
from ta_main_update_data import get_update_instr_data
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


def recalc_histdata(symbol):
    """
    Recalculate historical data for a specific instrument as per arg.
    Args:
        String: Symbol of the instrument to recalculate
    Returns:
        None
    """
    get_update_instr_data(1, True, symbol)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'UPDATE price_instruments_data SET is_ta_calc=0 WHERE symbol = "'+ str(symbol) +'"'
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    get_update_instr_data(1, True, symbol)
    print(str(symbol) + ': Done.')


print("###############################################################################")
print("Recalculate historical data for specific function")
print("-------------------------------------------------")
print("IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT")
print("recalc_histdata(symbol)")
print(" ")
print("provide the following parameters:")
print("(1) symbol")
print("--------------------------------------")
print("Affected tables/column:")
print("-----------------------")
print("1. price_instruments_data.*")
print("###############################################################################")
