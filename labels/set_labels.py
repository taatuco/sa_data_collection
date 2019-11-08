""" Import labels that are used by the programme into the db """
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


def set_labels():
    """
    Import labels for each available language into the database.
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
    sql = "DELETE FROM labels"
    cursor.execute(sql)
    connection.commit()

    ######## English ########
    lang_en = "en"
    portf_description_en = "This {market_asset_class} portfolio is designed by {nickname}."

    sql = "INSERT IGNORE INTO labels(lang, portf_description) VALUES "+\
    "('"+lang_en+"', '"+  portf_description_en +"') "
    debug(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

set_labels()
