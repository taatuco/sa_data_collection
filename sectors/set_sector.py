# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cr = connection.cursor(pymysql.cursors.SSCursor)

sql = "DELETE FROM sectors"
cr.execute(sql)

sql = "INSERT INTO sectors(id, sector) VALUES "+\
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
"('11','Treasury Bond'), "+\
"('12','Consumer Staples'), "+\
"('13','Energy'), "+\
"('14','Telecom and Services'), "+\
"('15','Real Estates'), "+\
"('18','Commodities')"


try:
    cr.execute(sql)
    connection.commit()
except Exception as e: print(e)
