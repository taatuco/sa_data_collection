""" Import Asset classes to db """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import pymysql.cursors
from settings import debug, SmartAlphaPath
from sa_access import sa_db_access

PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
SETT = SmartAlphaPath()

sys.path.append(os.path.abspath(SETT.get_path_pwd()))
ACCESS_OBJ = sa_db_access()

DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def set_asset_class():
    """
    Import asset classes to database.
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

    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "DELETE FROM asset_class"
    cursor.execute(sql)

    sql = "INSERT IGNORE INTO asset_class(asset_class_id, asset_class_name) VALUES "+\
    "('CR:','Crypto'), "+\
    "('EQ:','Stocks'), "+\
    "('FX:','Forex'), "+\
    "('PRF:','Portfolio'), "+\
    "('CO:','Commodities'), "+\
    "('BD:','Bonds'), "+\
    "('MA:','Multi-asset')"
    debug(sql +": "+ os.path.basename(__file__))

    cursor.execute(sql)
    connection.commit()
    cursor.close()


set_asset_class()
