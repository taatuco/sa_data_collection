""" Import Asset classes to db """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir))
from settings import debug, SmartAlphaPath
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import sa_db_access
access_obj = sa_db_access()

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()


def set_asset_class():
    """
    Import asset classes to database.
    Args:
        None
    Returns:
        None
    """
    import pymysql.cursors
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cr = connection.cursor(pymysql.cursors.SSCursor)

    sql = "DELETE FROM asset_class"
    cr.execute(sql)

    sql = "INSERT IGNORE INTO asset_class(asset_class_id, asset_class_name) VALUES "+\
    "('CR:','Crypto'), "+\
    "('EQ:','Stocks'), "+\
    "('FX:','Forex'), "+\
    "('PRF:','Portfolio'), "+\
    "('CO:','Commodities'), "+\
    "('BD:','Bonds'), "+\
    "('MA:','Multi-asset')"
    debug(sql +": "+ os.path.basename(__file__) )

    cr.execute(sql)
    connection.commit()
    cr.close()


set_asset_class()
