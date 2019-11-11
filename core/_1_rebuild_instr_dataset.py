""" First step of the process of rebuild data: Remove existing records """
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
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def rebuild_rm_existing_rec():
    """
    Remove existing records to prepare for the insert of new data.
    Args:
        None
    Returns:
        None
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    ################################################################################
    # Remove data from one day prior
    ################################################################################
    date_minus_one = datetime.datetime.now() - timedelta(days=1)
    date_minus_one = date_minus_one.strftime('%Y%m%d')

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'DELETE FROM price_instruments_data WHERE date >='+ str(date_minus_one)
    debug(sql)
    cursor.execute(sql)
    connection.commit()

    sql = 'DELETE FROM chart_data'
    debug(sql)
    cursor.execute(sql)
    connection.commit()

    sql = 'DELETE FROM feed WHERE type=1'
    debug(sql)
    cursor.execute(sql)
    connection.commit()

    sql = 'DELETE FROM trades'
    debug(sql)
    cursor.execute(sql)
    connection.commit()

    cursor.close()
    connection.close()

rebuild_rm_existing_rec()
