""" Functionalities related to moving average """
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
from settings import SmartAlphaPath
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def calc_ma(symbol_id, date_id, ma_period):
    """
    Compute moving average according to args
    Args:
        String: Instrument symbol
        String: Date in string format YYYYMMDD
        Integer: Moving average period
    Returns:
        Double: Moving average as per args
    """
    from_date = datetime.datetime.strptime(date_id, '%Y%m%d') - timedelta(days=ma_period)
    from_date = from_date.strftime("%Y%m%d")
    ma_period = str(ma_period)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT AVG(price_close) as ma FROM price_instruments_data "+\
    "WHERE symbol='"+symbol_id+"' AND date<="+date_id+" AND date>="+ from_date
    cursor.execute(sql)
    res = cursor.fetchall()
    mav = 0
    for row in res:
        mav = row[0]
    cursor.close()
    connection.close()
    return mav
