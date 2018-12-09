# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
from datetime import timedelta
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

sys.path.append(os.path.abspath( sett.get_path_signals() ))
from ta_instr_sum import *

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def get_portf_alloc():

    portf_symbol_suffix = get_portf_suffix()
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, symbol_list.uid, instruments.unit FROM instruments "+\
    "INNER JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol LIKE '"+portf_symbol_suffix+"%' ORDER BY instruments.symbol"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        portf_symbol = row[0]
        portf_fullname = row[1]
        portf_uid = row[2]
        portf_unit = row[3]
        portf_forc_return = 0
        portf_perc_return = 0
        portf_nav = 0
        alloc_forc_pnl = 0


        cr_pf = connection.cursor(pymysql.cursors.SSCursor)
        sql_pf = "SELECT symbol, quantity FROM portfolios WHERE portf_symbol ='"+ portf_symbol +"' ORDER BY portf_symbol"
        cr_pf.execute(sql_pf)
        rs_pf = cr_pf.fetchall()

        for row in rs_pf:
            print(sql_pf+": "+ os.path.basename(__file__) )
            portf_item_symbol = row[0]
            portf_item_quantity = row[1]


            cr_p = connection.cursor(pymysql.cursors.SSCursor)
            sql_p = "SELECT price_close, date FROM price_instruments_data WHERE symbol ='"+portf_item_symbol+"' ORDER BY date DESC LIMIT 1"
            cr_p.execute(sql_p)
            rs_p = cr_p.fetchall()
            print(sql_p+": "+ os.path.basename(__file__) )


            for row in rs_p:
                alloc_price = row[0]
                alloc_date = row[1]
                alloc_expiration = alloc_date + timedelta(days=7)
                alloc_expiration = alloc_expiration.strftime("%Y%m%d")

            cr_t = connection.cursor(pymysql.cursors.SSCursor)
            sql_t = "SELECT instruments.symbol, instruments.fullname, instruments.decimal_places, "+\
            "instruments.w_forecast_change, instruments.pip, symbol_list.uid FROM instruments "+\
            "INNER JOIN symbol_list ON instruments.symbol = symbol_list.symbol WHERE instruments.symbol ='"+portf_item_symbol+"'"

            cr_t.execute(sql_t)
            rs_t = cr_t.fetchall()
            print(sql_t+": "+ os.path.basename(__file__) )

            for row in rs_t:
                alloc_symbol = row[0]
                alloc_fullname = row[1]
                alloc_decimal_places = row[2]
                alloc_w_forecast_change = row[3]
                alloc_pip = row[4]
                alloc_uid = row[5]
                if alloc_w_forecast_change >= 0:
                    alloc_entry_level_sign = '<'
                    alloc_order_type = 'buy'
                else:
                    alloc_entry_level_sign = '>'
                    alloc_order_type = 'sell'
                alloc_dollar_amount = round( portf_item_quantity * alloc_price, int(alloc_decimal_places) ) * alloc_pip

                entry_level = alloc_entry_level_sign + ' ' + str( round( float(alloc_price), alloc_decimal_places) )

                print(portf_symbol +": " + alloc_symbol )

                cr_x = connection.cursor(pymysql.cursors.SSCursor)
                sql_x = 'UPDATE portfolios SET alloc_fullname="'+ alloc_fullname +'", order_type="' + alloc_order_type + '", '+\
                'dollar_amount='+ str(alloc_dollar_amount) +', entry_level="'+ entry_level +'", expiration='+ alloc_expiration +' '+\
                'WHERE symbol ="'+ alloc_symbol+'" AND portf_symbol ="' + portf_symbol + '" '
                print(sql_x)
                cr_x.execute(sql_x)
                connection.commit()

                alloc_forc_data = forecast_data(alloc_uid)
                alloc_forc_pnl =  alloc_forc_pnl + abs( (alloc_price - float(alloc_forc_data.get_frc_pt() )) * portf_item_quantity  )
                portf_forc_return = portf_forc_return + alloc_forc_pnl
                portf_nav = portf_nav + alloc_dollar_amount

        ### Updatedb
        portf_perc_return = (100/(portf_nav/portf_forc_return))/100
        w_forecast_display_info = portf_unit + " " + str( round(portf_forc_return,2) )
        cr_f = connection.cursor(pymysql.cursors.SSCursor)
        sql_f = "UPDATE instruments SET w_forecast_change=" + str(portf_perc_return) + ", w_forecast_display_info='" + w_forecast_display_info + "' " +\
        "WHERE symbol='"+portf_symbol+"' "
        cr_f.execute(sql_f)
