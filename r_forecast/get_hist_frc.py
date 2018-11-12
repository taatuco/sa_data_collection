# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
from datetime import timedelta
import csv
from pathlib import Path

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

import pymysql.cursors
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


frc_pt = 0

forc_src = sett.get_path_src()
ext = ".csv"

cr = connection.cursor(pymysql.cursors.SSCursor)
sql = "SELECT symbol, uid FROM symbol_list ORDER BY symbol"
cr.execute(sql)
rs = cr.fetchall()
for row in rs:
    uid = row[1]
    s = row[0]

    i = 0
    t = 360
    while i <= 360:
        file_str = forc_src+str(uid)+'f.csv'
        filepath = Path(file_str)
        if filepath.exists():
            with open(file_str) as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                i = 1
                for row in readCSV:
                    if (i == 8):
                        frc_pt = row[1]
                    i +=1
        i+=1
