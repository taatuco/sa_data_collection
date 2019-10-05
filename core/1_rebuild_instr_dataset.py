# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
from pathlib import Path
from send_mail import *
import datetime
import time
from datetime import timedelta

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

################################################################################
# Remove data from one day prior
################################################################################
dy = datetime.datetime.now() - timedelta(days=1)
dy = dta.strftime('%Y%m%d')

cr = connection.cursor(pymysql.cursors.SSCursor)
sql = 'DELETE FROM price_instruments_data WHERE date >='+ str(dy)
print(sql)
cr.execute(sql)
connection.commit()

sql = 'DELETE FROM chart_data'
print(sql)
cr.execute(sql)
connection.commit()

sql = 'DELETE FROM feed WHERE type=1'
print(sql)
cr.execute(sql)
connection.commit()
