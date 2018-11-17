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

sys.path.append(os.path.abspath( sett.get_path_portfolios() ))
from set_portf_alloc import *


import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


portf_symbol_suffix = '#PRF:'
cr = connection.cursor(pymysql.cursors.SSCursor)


set_portf_fx()
set_portf_crypto()
set_portf_commo()
set_portf_multi()
set_portf_us()



def set_portf_fx():
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except:
        pass
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE','No-Fly Zone Airspace','FX:','GO>',5,10000)"
    try:
        cr.execute(sql)
        connection.commit()
        set_alloc(portf_symbol_suffix, "FXONE")
    except:
        pass

def set_portf_crypto():
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except:
        pass
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE','The Hot Potato','CR:','GO>',5,1)"
    try:
        cr.execute(sql)
        connection.commit()
        set_alloc(portf_symbol_suffix, "CRYPTONE")
    except:
        pass

def set_portf_commo():
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except:
        pass
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE','Gold Digger','CO:','GO>',2,1)"
    try:
        cr.execute(sql)
        connection.commit()
        set_alloc(portf_symbol_suffix, "COMMONE")
    except:
        pass

def set_portf_multi():
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE'), "+\
    "('" + portf_symbol_suffix + "GOJONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except:
        pass
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE','Milkshake','MA:','GO>',5,1), "+\
    "('" + portf_symbol_suffix + "GOJONE','Safe Haven','MA','GO>',5,1)"
    try:
        cr.execute(sql)
        connection.commit()
        set_alloc(portf_symbol_suffix, "MULTIONE")
        set_alloc(portf_symbol_suffix, "GOJONE")
    except:
        pass

def set_portf_us():
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "INDXONE'), "+\
    "('" + portf_symbol_suffix + "INDUONEUS'), "+\
    "('" + portf_symbol_suffix + "TECHONEUS'), "+\
    "('" + portf_symbol_suffix + "HCONEUS'), "+\
    "('" + portf_symbol_suffix + "CDONEUS'), "+\
    "('" + portf_symbol_suffix + "UTILONEUS'), "+\
    "('" + portf_symbol_suffix + "FINONEUS'), "+\
    "('" + portf_symbol_suffix + "MATONEUS'), "+\
    "('" + portf_symbol_suffix + "TONEUS'), "+\
    "('" + portf_symbol_suffix + "CSONEUS'), "+\
    "('" + portf_symbol_suffix + "NRGONEUS'), "+\
    "('" + portf_symbol_suffix + "TELCONEUS'), "+\
    "('" + portf_symbol_suffix + "REITONEUS'), "+\
    "('" + portf_symbol_suffix + "FOODONEUS'), "+\
    "('" + portf_symbol_suffix + "DEFONEUS'), "+\
    "('" + portf_symbol_suffix + "TOBACONEUS')"
    try:
        cr.execute(sql)
        connection.commit()
    except:
        pass
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip) VALUES "+\
    "('" + portf_symbol_suffix + "INDXONE','The Escalator','EQ:','GO>',2,1), "+\
    "('" + portf_symbol_suffix + "INDUONEUS','Smoke Up','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "TECHONEUS','Time Travel','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "HCONEUS','Dr Kahroo','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "CDONEUS','Rich Kids','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "UTILONEUS','Uncle James','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "FINONEUS','Piggy Bank','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "MATONEUS','Iron String','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "TONEUS','Snail','BD:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "CSONEUS','Bread and Milk','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "NRGONEUS','The Fast and the Furious','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "TELCONEUS','The Phone Booth','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "REITONEUS','House of Cards','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "FOODONEUS','Burritos','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "DEFONEUS','Guns and ROses','EQ:','US>',2,1), "+\
    "('" + portf_symbol_suffix + "TOBACONEUS','Party don-t stop','EQ:','US>',2,1)"
    try:
        cr.execute(sql)
        connection.commit()
        set_alloc(portf_symbol_suffix, "INDXONE")
        set_alloc(portf_symbol_suffix, "INDUONEUS")
        set_alloc(portf_symbol_suffix, "TECHONEUS")
        set_alloc(portf_symbol_suffix, "HCONEUS")
        set_alloc(portf_symbol_suffix, "CDONEUS")
        set_alloc(portf_symbol_suffix, "UTILONEUS")
        set_alloc(portf_symbol_suffix, "FINONEUS")
        set_alloc(portf_symbol_suffix, "MATONEUS")
        set_alloc(portf_symbol_suffix, "TONEUS")
        set_alloc(portf_symbol_suffix, "CSONEUS")
        set_alloc(portf_symbol_suffix, "NRGONEUS")
        set_alloc(portf_symbol_suffix, "TELCONEUS")
        set_alloc(portf_symbol_suffix, "REITONEUS")
        set_alloc(portf_symbol_suffix, "FOODONEUS")
        set_alloc(portf_symbol_suffix, "DEFONEUS")
        set_alloc(portf_symbol_suffix, "TOBACONEUS")
    except:
        pass
