""" Import financial sectors into the database """
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

def set_sector():
    """
    Import financial sectors into the database
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
    sql = "DELETE FROM sectors"
    cursor.execute(sql)
    sql = "INSERT IGNORE INTO sectors(id, sector) VALUES "+\
    "('1','FX'), "+\
    "('2','Cryptocurrency'), "+\
    "('17','Index'), "+\
    "('4','Industrials'), "+\
    "('5','Technology'), "+\
    "('6','Health Care'), "+\
    "('7','Consumer Discretionary'), "+\
    "('8','Utilities'), "+\
    "('9','Financials'), "+\
    "('10','Materials'), "+\
    "('11','Treasury Bond / Government Bond'), "+\
    "('12','Consumer Staples'), "+\
    "('13','Energy'), "+\
    "('14','Telecom and Services'), "+\
    "('15','Real Estates'), "+\
    "('19','Multi-asset / Multi-sector'), "+\
    "('18','Commodities')"
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

set_sector()
