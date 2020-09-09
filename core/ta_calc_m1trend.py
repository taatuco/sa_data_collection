""" Functionalities related to moving average """
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

def calc_m1trend(symbol_id, date_id, connection):
    """
    Compute m1trend which is previous period price.
    Args:
        String: Instrument symbol
        String: Date in string format YYYYMMDD
        String connection string
    Returns:
        Double: previous price as per args
    """

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT price_close FROM price_instruments_data "+\
    "WHERE symbol='"+symbol_id+"' AND date<"+date_id+" ORDER BY date DESC LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    ret = 0
    for row in res:
        ret = row[0]
    cursor.close()
    return ret