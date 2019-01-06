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

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

sys.path.append(os.path.abspath( sett.get_path_feed() ))
from add_feed_type import *

sys.path.append(os.path.abspath( sett.get_path_core() ))
from get_instr_perf_summ import *
from sa_numeric import *

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def get_portf_perf_summ(s,uid):
    pps = instr_sum_data(s, uid)
    y1 = pps.get_pct_1Yp(); m6 = pps.get_pct_6Mp(); m3 = pps.get_pct_3Mp(); m1 = pps.get_pct_1Mp(); w1 = pps.get_pct_1Wp()
    dm = datetime.datetime.now() - timedelta(days=30) ; dm = dm.strftime('%Y%m%d')
    sql = "SELECT price_close FROM chart_data WHERE uid="+ str(uid) +" AND date >="+ str(dm) +" ORDER BY date"
    stdev_st = get_stdev(sql)
    maximum_dd_st = get_mdd(sql)
    romad_st = get_romad(sql)
    volatility_risk_st = get_volatility_risk(sql,True,s)

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "UPDATE instruments SET y1="+ str(y1) +", m6="+ str(m6) +", m3="+ str(m3) +", m1="+ str(m1) +", w1="+ str(w1) +", "+\
    " stdev_st="+ str(stdev_st) + ", maximum_dd_st="+ str(maximum_dd_st) + ", romad_st="+ str(romad_st) + ", volatility_risk_st="+ str(volatility_risk_st) +\
    " WHERE symbol='"+ str(s)  +"' "
    cr.execute(sql)
    connection.commit()

def get_portf_perf():
    portf_symbol_suffix = get_portf_suffix()
    df = datetime.datetime.now() - timedelta(days=370)

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.symbol, symbol_list.uid, instruments.fullname, instruments.account_reference "+\
    "FROM `symbol_list` INNER JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.symbol LIKE '"+portf_symbol_suffix+"%' ORDER BY symbol_list.symbol"
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        portf_symbol = row[0]
        portf_uid = row[1]
        portf_fullname = row[2]
        account_reference = row[3]

        i = 0
        j = 370
        d = df
        portf_nav = account_reference

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM chart_data WHERE uid = "+ str(portf_uid)
        print(sql_i)
        cr_i.execute(sql_i)
        connection.commit()

        while (i <= j):

            d = d + timedelta(days=1)
            d_str = d.strftime("%Y%m%d")
            portf_pnl = 0
            portf_content = ''

            #get portfolio allocations
            #for each item get the pnl
            if d < datetime.datetime.now():
                cr_c = connection.cursor(pymysql.cursors.SSCursor)
                sql_c = "SELECT price_instruments_data.pnl, portfolios.quantity, instruments.pip " +\
                "FROM portfolios JOIN price_instruments_data ON portfolios.symbol = price_instruments_data.symbol "+\
                "JOIN instruments ON portfolios.symbol = instruments.symbol "+\
                "WHERE portfolios.portf_symbol = '"+ portf_symbol +"' AND date="+ d_str +" ORDER BY portfolios.portf_symbol"
                print(sql_c)

                cr_c.execute(sql_c)
                rs_c = cr_c.fetchall()

                for row in rs_c:
                    pnl_c = row[0]
                    quantity_c = row[1]
                    pip_c = row[2]
                    portf_pnl = portf_pnl + (pnl_c * quantity_c * pip_c)
                    portf_content = portf_content +" (" + str(pnl_c) + " * "+ str(quantity_c) +") "
                cr_c.close()
                portf_nav = round( portf_nav + portf_pnl, 2)

                try:

                    sql_i = "INSERT INTO chart_data(uid, symbol, date, price_close) "+\
                    "VALUES (" + str(portf_uid) + ",'"+ str(portf_symbol) +"','" + str(d_str) + "'," + str(portf_nav) + ")"
                    print(sql_i)
                    cr_i.execute(sql_i)
                    connection.commit()

                except Exception as e: print(e)

            i +=1
        cr_i.close()
        get_portf_perf_summ(portf_symbol, portf_uid)
    cr.close()
