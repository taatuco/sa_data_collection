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

sys.path.append(os.path.abspath( sett.get_path_feed() ))
from add_feed_type import *

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_portf_perf():
    portf_symbol_suffix = '#PRF:'
    df = datetime.datetime.now() - timedelta(days=360)

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.symbol, symbol_list.uid, instruments.fullname "+\
    "FROM `symbol_list` INNER JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.symbol LIKE '"+portf_symbol_suffix+"%' ORDER BY symbol_list.symbol"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        portf_symbol = row[0]
        portf_uid = row[1]
        portf_fullname = row[2]

        i = 0
        j = 360
        d = df
        portf_nav = 0

        f = sett.get_path_src()+"\\"+str(portf_uid)+"pp.csv"
        with open(f, 'w', newline='') as csvfile:
            fieldnames = ["portf_fullname","date","portf_nav", "portf_content"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            while (i <= j):

                d = d + timedelta(days=1)
                d_str = d.strftime("%Y%m%d")
                portf_pnl = 0
                portf_content = ''

                #get portfolio allocations
                #for each item get the pnl
                cr_c = connection.cursor(pymysql.cursors.SSCursor)
                sql_c = "SELECT price_instruments_data.pnl, portfolios.quantity " +\
                "FROM portfolios INNER JOIN price_instruments_data ON portfolios.symbol = price_instruments_data.symbol "+\
                "WHERE portfolios.portf_symbol = '"+ portf_symbol +"' AND date="+ d_str +" ORDER BY portfolios.portf_symbol"

                print(sql_c)

                cr_c.execute(sql_c)
                rs_c = cr_c.fetchall()

                for row in rs_c:
                    pnl_c = row[0]
                    quantity_c = row[1]
                    portf_pnl = portf_pnl + (pnl_c * quantity_c)
                    portf_content = portf_content +" (" + str(pnl_c) + " * "+ str(quantity_c) +") " 
                portf_nav = portf_nav + portf_pnl

                writer.writerow({"portf_fullname": str(portf_fullname),
                "date": str(d_str),"portf_nav": str(portf_nav), "portf_content": str(portf_content) })


                i +=1
