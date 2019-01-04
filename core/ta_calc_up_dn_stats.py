# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import csv
import gc

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

def get_count_d(s,t,p):
    try:
        cnt = 0
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql_select = "SELECT COUNT(id) FROM price_instruments_data WHERE symbol = '"+ s +"' "

        if (t == 1):
            sql_t_cond = "AND change_1d>=0 "
        else:
            sql_t_cond = "AND change_1d<0 "

        sql_p_cond = " AND date>= DATE(DATE_ADD(curdate(), INTERVAL -"+ str(p) +" DAY))"

        sql = sql_select + sql_t_cond + sql_p_cond
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            cnt = row[0]

        return cnt

    except:
        pass

def get_day_up_dwn_stat(s,uid):

    m1_up = get_count_d(s,1,30)
    m1_dn = get_count_d(s,-1,30)
    w1_up = get_count_d(s,1,7)
    w1_dn = get_count_d(s,-1,7)

    f = sett.get_path_src()+"\\"+str(uid)+"ud.csv"
    with open(f, 'w', newline='') as csvfile:
        fieldnames = ["symbol","7_up_days","7_down_days","30_up_days", "30_down_days"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print(s +": "+ os.path.basename(__file__) )
        writer.writerow({"symbol": str(s),
        "7_up_days": str(w1_up),"7_down_days": str(w1_dn),
        "30_up_days": str(m1_up),"30_down_days": str(m1_dn) })
