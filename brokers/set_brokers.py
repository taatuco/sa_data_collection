""" Import brokers and affiliate links to the database """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import debug, SmartAlphaPath
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access

ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def set_brokers():
    """
    Import brokers and affiliate link to the database.
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

    sql = "DELETE FROM brokers"
    cursor.execute(sql)
    sql = """
    INSERT IGNORE INTO brokers(broker_id, burl, affiliate_link) VALUES
    ('eToro','https://www.etoro.com/markets/','http://partners.etoro.com/A52784_TClick.aspx'),
    ('googleSiteSmartAlpha','https://sites.google.com/view/','https://sites.google.com/view/about-smartalpha'),
    ('Tradingview','https://app.smartalphatrade.com/s/','20367')
    """
    debug(sql +": "+ os.path.basename(__file__))
    cursor.execute(sql)
    connection.commit()
    cursor.close()

set_brokers()
