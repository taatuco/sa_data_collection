# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


cr = connection.cursor(pymysql.cursors.SSCursor)
sql = "DELETE FROM labels"
cr.execute(sql)
connection.commit()


######## English ########
lang_en = "en"
portf_description_en ="This {market_asset_class} portfolio is designed by {nickname}."


sql = "INSERT IGNORE INTO labels(lang, portf_description) VALUES "+\
"('"+lang_en+"', '"+  portf_description_en +"') "
debug(sql)

try:
    cr.execute(sql)
    connection.commit()
except Exception as e: debug(e)

cr.close()
connection.close()
