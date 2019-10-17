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
import random

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
from ta_instr_sum import *

from pathlib import Path

import pymysql.cursors

class portf_data:

    portf_multip = 0
    portf_big_alloc_price = 0
    portf_total_alloc_amount = 0
    portf_account_ref = 0

    def __init__(self, portf_s):

        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT account_reference FROM instruments WHERE symbol='"+ portf_s +"' "
        cr.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            self.portf_account_ref = row[0]
        cr.close()

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol FROM portfolios WHERE portf_symbol = '"+ portf_s +"'"
        cr.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            cr_s = connection.cursor(pymysql.cursors.SSCursor)
            sql_s = "SELECT instruments.pip, price_instruments_data.price_close "+\
            "FROM instruments JOIN price_instruments_data ON instruments.symbol = price_instruments_data.symbol "+\
            "WHERE price_instruments_data.symbol='"+ str(row[0]) +"' "+\
            "ORDER BY price_instruments_data.date DESC LIMIT 1"
            cr_s.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
            cr_s.execute(sql_s)
            rs_s = cr_s.fetchall()
            for row in rs_s:
                pip_s = row[0]
                price_s = row[1]
                salloc = int( pip_s * price_s )
                if salloc > self.portf_big_alloc_price:
                    self.portf_big_alloc_price = salloc
                self.portf_total_alloc_amount = self.portf_total_alloc_amount + salloc
            cr_s.close()
        cr.close()
        connection.close()
        try:
            self.portf_multip = self.portf_account_ref / self.portf_total_alloc_amount
        except:
            self.portf_multip = 1

    def get_quantity(self, alloc_s, alloc_coef):

        portf_reduce_risk_by = 4

        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT instruments.pip, price_instruments_data.price_close, instruments.volatility_risk_st "+\
        "FROM instruments JOIN price_instruments_data ON instruments.symbol = price_instruments_data.symbol "+\
        "WHERE price_instruments_data.symbol='"+ alloc_s +"' "+\
        "ORDER BY price_instruments_data.date DESC LIMIT 1"
        cr.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
        cr.execute(sql)
        rs = cr.fetchall()
        q = 0
        for row in rs:
            pip_s = row[0]
            price_s = row[1]
            volatility_risk_st = row[2]
            salloc = ( pip_s * price_s )
        cr.close()
        connection.close()

        portf_reduce_risk_by = round(volatility_risk_st * 200,0)
        if portf_reduce_risk_by < 1: portf_reduce_risk_by = 4

        q = round( (( (self.portf_big_alloc_price / salloc) * self.portf_multip ) / portf_reduce_risk_by )*alloc_coef , 2)
        if q < 0.01:
            q = 0.01

        if q > 1:
            q = int(q)
            if q == 0:
                q = 1

        return q


def get_conviction_coef(c):
    r = 1.01
    try:
        if c == 'weak': r = random.randint(3,8)
        if c == 'neutral': r = random.randint(8,20)
        if c == 'strong': r = random.randint(21,80)
        r = (r * 0.01) + 1
    except Exception as e: debug(e)
    return r

def get_market_conv_rate(m):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT conv_to_usd FROM markets WHERE market_id = '"+ str(m) +"'"
        cr.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
        connection.close()
    except Exception as e: debug(e)
    return r

def get_market_currency(m):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT currency_code FROM markets WHERE market_id = '"+ str(m) +"'"
        cr.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
        connection.close()
    except Exception as e: debug(e)
    return r

def get_portf_alloc():

    portf_symbol_suffix = get_portf_suffix()
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, symbol_list.uid, instruments.unit, instruments.market FROM instruments "+\
    "INNER JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol LIKE '"+portf_symbol_suffix+"%' ORDER BY instruments.symbol"
    cr.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        portf_symbol = row[0]
        portf_fullname = row[1]
        portf_uid = row[2]
        portf_unit = row[3]
        portf_market = row[4]
        portf_currency = get_market_currency(portf_market)
        portf_forc_return = 0
        portf_perc_return = 0
        portf_nav = 0
        alloc_forc_pnl = 0

        portfd = portf_data(portf_symbol)

        cr_pf = connection.cursor(pymysql.cursors.SSCursor)
        sql_pf = "SELECT symbol, quantity, strategy_conviction FROM portfolios WHERE portf_symbol ='"+ portf_symbol +"' ORDER BY portf_symbol"
        cr_pf.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
        cr_pf.execute(sql_pf)
        rs_pf = cr_pf.fetchall()
        for row in rs_pf:

            debug(sql_pf+": "+ os.path.basename(__file__) )
            portf_item_symbol = row[0]
            portf_initial_item_quantity = row[1]
            portf_item_conviction = row[2]
            portf_item_conviction_coef = get_conviction_coef(portf_item_conviction)
            if portf_initial_item_quantity == 1:
                portf_item_quantity = portfd.get_quantity(portf_item_symbol,portf_item_conviction_coef)
            else:
                portf_item_quantity = portf_initial_item_quantity

            cr_p = connection.cursor(pymysql.cursors.SSCursor)
            sql_p = "SELECT price_close, date FROM price_instruments_data WHERE symbol ='"+portf_item_symbol+"' ORDER BY date DESC LIMIT 1"
            cr_p.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
            cr_p.execute(sql_p)
            rs_p = cr_p.fetchall()
            debug(sql_p+": "+ os.path.basename(__file__) )
            for row in rs_p:
                alloc_price = row[0]
                alloc_date = row[1]
                alloc_expiration = alloc_date + timedelta(days=7)
                alloc_expiration = alloc_expiration.strftime("%Y%m%d")
            cr_p.close()

            cr_t = connection.cursor(pymysql.cursors.SSCursor)
            sql_t = "SELECT instruments.symbol, instruments.fullname, instruments.decimal_places, "+\
            "instruments.w_forecast_change, instruments.pip, symbol_list.uid, instruments.market FROM instruments "+\
            "INNER JOIN symbol_list ON instruments.symbol = symbol_list.symbol WHERE instruments.symbol ='"+portf_item_symbol+"'"
            cr_t.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
            cr_t.execute(sql_t)
            rs_t = cr_t.fetchall()
            debug(sql_t+": "+ os.path.basename(__file__) )

            for row in rs_t:
                alloc_symbol = row[0]
                alloc_fullname = row[1]
                alloc_decimal_places = row[2]
                alloc_w_forecast_change = row[3]
                alloc_pip = row[4]
                alloc_uid = row[5]
                alloc_market = row[6]
                if alloc_w_forecast_change >= 0:
                    alloc_entry_level_sign = '<'
                    alloc_order_type = 'buy'
                else:
                    alloc_entry_level_sign = '>'
                    alloc_order_type = 'sell'

                if portf_currency != 'USD':
                    alloc_conv_rate = 1
                else:
                    alloc_conv_rate = get_market_conv_rate(alloc_market)

                alloc_dollar_amount = round( portf_item_quantity * alloc_price * alloc_conv_rate, int(alloc_decimal_places) ) * alloc_pip
                portf_item_quantity = round(portf_item_quantity / alloc_conv_rate,2)
                if portf_item_quantity < 0.01: portf_item_quantity = 0.01


                entry_level = alloc_entry_level_sign + ' ' + str( round( float(alloc_price), alloc_decimal_places) )

                debug(portf_symbol +": " + alloc_symbol )

                cr_x = connection.cursor(pymysql.cursors.SSCursor)
                sql_x = 'UPDATE portfolios SET quantity='+ str(portf_item_quantity) +', alloc_fullname="'+ alloc_fullname +'", order_type="' + alloc_order_type + '", '+\
                'dollar_amount='+ str(alloc_dollar_amount) +', entry_level="'+ entry_level +'", expiration='+ alloc_expiration +' '+\
                'WHERE symbol ="'+ alloc_symbol+'" AND portf_symbol ="' + portf_symbol + '" '
                debug(sql_x)
                cr_x.execute(sql_x)
                connection.commit()
                cr_x.close()

                alloc_forc_data = forecast_data(alloc_uid)
                alloc_forc_pnl =  alloc_forc_pnl + abs( (alloc_price - float(alloc_forc_data.get_frc_pt() )) * portf_item_quantity * alloc_pip )
                portf_forc_return = portf_forc_return + alloc_forc_pnl
                portf_nav = portf_nav + alloc_dollar_amount
            cr_t.close()
        cr_pf.close()
        ### Updatedb
        try:
            portf_perc_return = (100/(portf_nav/portf_forc_return))/100
        except:
            portf_perc_return = 0

        w_forecast_display_info = "+" + portf_unit + " " + str( round(portf_forc_return,2) )
        cr_f = connection.cursor(pymysql.cursors.SSCursor)
        sql_f = "UPDATE instruments SET w_forecast_change=" + str(portf_perc_return) + ", w_forecast_display_info='" + w_forecast_display_info + "' " +\
        "WHERE symbol='"+portf_symbol+"' "
        cr_f.execute(sql_f)
        connection.commit()
        cr_f.close()
    cr.close()
    connection.close()
