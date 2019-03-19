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

import pymysql.cursors
db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def set_portf_symbol():
    r = ''
    try:
        symbol = ''
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT part_three FROM randwords ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: symbol = symbol + row[0]
        symbol = symbol + str( random.randint(1,999) )
        r = get_portf_suffix() + symbol.upper()
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def set_portf_fullname(s,ac,m,st):
    #portf: symbol, asset_class_name, market_label, strategy_type
    r = ''
    try:
        fullname = s.replace(get_portf_suffix(),'')
        r = fullname + ' ' + m + ' ' + ac + ' ' + st
    except Exception as e: print(e)
    return r

def get_portf_description(ac,m,st):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portf_description FROM labels WHERE lang = '"+ "en" +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: portf_description = row[0]
        nickname = get_nickname()
        market_asset_class = ac + ' ' + m + ' '+ st
        portf_description = portf_description.replace('{market_asset_class}',market_asset_class)
        portf_description = portf_description.replace('{nickname}',nickname)
        r = portf_description
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_strategy():
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT codename FROM strategies ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r

def get_asset_class_name(ac):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT asset_class_name FROM asset_class WHERE asset_class_id='"+ str(ac) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r

def get_market_name(m):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT market_label FROM markets WHERE market_id='"+ str(ac) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r

def get_decimal_places(ac):
    r = 2
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT decimal_places FROM asset_class WHERE asset_class = '"+ str(ac) +"' ORDER BY decimal_places DESC LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r

def get_unit(m):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT currency_code FROM markets WHERE market_id = '"+ str(m) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r

def set_portf_owner():
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT id FROM users WHERE is_bot=1 ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r

def select_allocation(ac,m):
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol FROM instruments WHERE symbol NOT LIKE '%"+ get_portf_suffix() +"%' AND asset_class = '"+ str(ac) +"' AND market = '"+ str(m) +"' ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r

def gen_portf_allocation(s,ac,m,sy):
    try:
        strategy_order_type = 'long/short'
        if sy == 'l': strategy_order_type = 'long'
        if sy == 's': strategy_order_type = 'short'
        strategy_conviction = 'neutral'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)

        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"')"
        print(sql)
        cr.execute(sql)
        connection.commit()
        cr.close()
        connection.close()
    except Exception as e: print(e)

def create_portf(ac,m,sy):
    try:
        st = ''
        if sy =='ls': st = 'long/short'
        if sy =='s': st = 'ultra short'

        portf_symbol = set_portf_symbol()
        asset_class_id = ac
        market_id = m
        fullname = set_portf_fullname(portf_symbol, get_asset_class_name(ac), get_market_name(m), st)
        decimal_places = get_decimal_places(ac)
        pip = 1
        sector = 0
        unit = get_unit(m)
        portf_description = get_portf_description(ac,m,st)
        account_reference = 1000
        portf_owner = set_portf_owner()

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
        "('"+ portf_symbol +"')"
        print(sql)
        cr.execute(sql)
        connection.commit()
        sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
        "('"+ str(portf_symbol) +"','"+ str(fullname) +"','"+ str(asset_class_id) +"','"+ str(market_id) +"',"+ str(decimal_places) +","+ str(pip) +","+ str(sector) +",'"+ str(unit) +"','"+ str(portf_description) +"',"+ str(account_reference) +","+ str(portf_owner) +")"
        print(sql)
        cr.execute(sql)
        connection.commit()

        gen_portf_allocation(portf_symbol,ac,m,sy)

        cr.close()
        connection.close()

    except Exception as e: print(e)

def gen_portf():
    try:

        #Scan Asset Class and create portfolio if not reach threshold
        min_portf_threshold = 200
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT asset_class_id FROM asset_class WHERE asset_class_id <> 'PF:' AND asset_class_id <> 'MA:' AND asset_class_id <>'BD:' AND asset_class_id <>'CO:' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            asset_class_id = row[0]
            if asset_class_id == 'CR:' or asset_class_id == 'FX:':
                market_id = 'GO>'
                for i in range(min_portf_threshold):
                    create_portf(asset_class_id,market_id, get_strategy() )
            else:
                cr_m = connection.cursor(pymysql.cursors.SSCursor)
                sql_m = "SELECT market_id FROM markets WHERE market_id <> 'GO>' "
                cr_m.execute(sql_m)
                rs_m = cr_m.fetchall()
                for row in rs_m:
                    market_id = row[0]
                    for i in range(min_portf_threshold):
                        create_portf(asset_class_id,market_id, get_strategy() )

        cr.close()
        cr_m.close()
        connection.close()

    except Exception as e: print(e)

gen_portf()
