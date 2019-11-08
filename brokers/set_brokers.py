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

sql = "DELETE FROM brokers"
cr.execute(sql)

sql = "INSERT IGNORE INTO brokers(broker_id, burl, affiliate_link) VALUES "+\
"('eToro','https://www.etoro.com/markets/','http://partners.etoro.com/A52784_TClick.aspx'),"+\
"('googleSiteSmartAlpha','https://sites.google.com/view/','https://sites.google.com/view/about-smartalpha')"+\
"('Tradingview','https://tradingview.com/','20367')"

debug(sql +": "+ os.path.basename(__file__) )

try:
    cr.execute(sql)
    connection.commit()
    cr.close()
except Exception as e: debug(e)
