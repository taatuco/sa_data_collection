# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
import time
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

def get_portf_alloc():

    portf_symbol_suffix = '#PRF:'
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, symbol_list.uid FROM instruments "+\
    "INNER JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol LIKE '"+portf_symbol_suffix+"%' ORDER BY instruments.symbol"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        portf_symbol = row[0]
        portf_fullname = row[1]
        portf_uid = row[2]

        f = sett.get_path_src()+"\\"+str(portf_uid)+"pf.csv"
        with open(f, 'w', newline='') as csvfile:
            fieldnames = ["portf_uid","portf_fullname","alloc_order_type","portf_item_quantity","alloc_symbol","alloc_fullname","alloc_dollar_amount"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


            cr_pf = connection.cursor(pymysql.cursors.SSCursor)
            sql_pf = "SELECT symbol, quantity FROM portfolios WHERE portf_symbol ='"+ portf_symbol +"' ORDER BY portf_symbol"
            cr_pf.execute(sql_pf)
            rs_pf = cr_pf.fetchall()

            for row in rs_pf:
                print(sql_pf+": "+ os.path.basename(__file__) )
                portf_item_symbol = row[0]
                portf_item_quantity = row[1]


                cr_p = connection.cursor(pymysql.cursors.SSCursor)
                sql_p = "SELECT price_close FROM price_instruments_data WHERE symbol ='"+portf_item_symbol+"' ORDER BY date DESC LIMIT 1"
                cr_p.execute(sql_p)
                rs_p = cr_p.fetchall()
                print(sql_p+": "+ os.path.basename(__file__) )


                for row in rs_p:
                    alloc_price = row[0]

                cr_t = connection.cursor(pymysql.cursors.SSCursor)
                sql_t = "SELECT symbol, fullname, decimal_places, w_forecast_change, pip FROM instruments WHERE symbol ='"+portf_item_symbol+"' "
                cr_t.execute(sql_t)
                rs_t = cr_t.fetchall()
                print(sql_t+": "+ os.path.basename(__file__) )

                for row in rs_t:
                    alloc_symbol = row[0]
                    alloc_fullname = row[1]
                    alloc_decimal_places = row[2]
                    alloc_w_forecast_change = row[3]
                    alloc_pip = row[4]
                    if alloc_w_forecast_change >= 0:
                        alloc_order_type = 'buy'
                    else:
                        alloc_order_type = 'sell'
                    alloc_dollar_amount = round( portf_item_quantity * alloc_price, int(alloc_decimal_places) ) * alloc_pip

                    print(portf_symbol +": " + alloc_symbol )
                    writer.writerow({"portf_uid": str(portf_uid),"portf_fullname": str(portf_fullname),
                    "alloc_order_type": str(alloc_order_type),"portf_item_quantity": str(portf_item_quantity),
                    "alloc_symbol": str(alloc_symbol),"alloc_fullname": str(alloc_fullname), "alloc_dollar_amount": str(alloc_dollar_amount) })

                    ### Compute expected return in dollar amount and in percentage ###
