# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

######################
symbol ="NYSE:BA"
uid = 214
######################
import sys
import os
import time

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

import csv
csvdir = sett.get_path_r_quantmod_src()
from pathlib import Path

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

import csv
csvdir = sett.get_path_r_quantmod_src()
from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

s = symbol
file_str = csvdir+str(uid)+'.csv'
filepath = Path(file_str)
if filepath.exists():
    with open(file_str) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            time.sleep(0.2)
            price_date = row[0]
            price_date = price_date.replace('.', '-')
            price_date = price_date.replace('X', '')
            price_date = price_date.replace('-','')
            price_date = '%.8s' % price_date
            price_close = row[4]
            print(s +": "+price_date+": "+ os.path.basename(__file__) )
            if price_close != "open" and price_close != "NA":
                try:
                    cr_q_ins = connection.cursor(pymysql.cursors.SSCursor)
                    sql_q_ins = "INSERT INTO price_instruments_data (symbol, date, price_close) VALUES ('"+s+"',"+price_date+","+price_close+");"
                    cr_q_ins.execute(sql_q_ins)
                    connection.commit()
                    cr_q_ins.close()
                except:
                    pass
else:
    print(file_str + "Not exists")