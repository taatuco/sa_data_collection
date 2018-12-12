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


portf_symbol_suffix = get_portf_suffix()
cr = connection.cursor(pymysql.cursors.SSCursor)
sql = "DELETE FROM instruments WHERE symbol LIKE '" + portf_symbol_suffix + "%' "
cr.execute(sql)
sql = "DELETE FROM symbol_list WHERE symbol LIKE '"+ portf_symbol_suffix +"%' "
cr.execute(sql)

def set_portf_fx():
    ac = "fx"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE','No-Fly Zone Airspace','FX:','GO>',5,10000,1,'USD')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "FXONE") )
    return ac

def set_portf_crypto():
    ac = "crypto"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE','The Hot Potato','CR:','GO>',5,1,2,'USD')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "CRYPTONE") )
    return ac

def set_portf_commo():
    ac = "commo"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE','Gold Digger','CO:','GO>',2,1,18,'USD')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "COMMONE") )
    return ac

def set_portf_multi():
    ac = "multi"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE'), "+\
    "('" + portf_symbol_suffix + "GOJONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE','Milkshake','MA:','GO>',5,1,19,'USD'), "+\
    "('" + portf_symbol_suffix + "GOJONE','Safe Haven','MA:','GO>',5,1,19,'USD')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "MULTIONE") )
    print( set_alloc(portf_symbol_suffix, "GOJONE") )
    return ac

def set_portf_us():
    ac = "us"
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
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit) VALUES "+\
    "('" + portf_symbol_suffix + "INDXONE','The Escalator','EQ:','GO>',2,1,17,'USD'), "+\
    "('" + portf_symbol_suffix + "INDUONEUS','Smoke Up','EQ:','US>',2,1,4,'USD'), "+\
    "('" + portf_symbol_suffix + "TECHONEUS','Time Travel','EQ:','US>',2,1,5,'USD'), "+\
    "('" + portf_symbol_suffix + "HCONEUS','Dr Kam','EQ:','US>',2,1,6,'USD'), "+\
    "('" + portf_symbol_suffix + "CDONEUS','Rich Kids','EQ:','US>',2,1,7,'USD'), "+\
    "('" + portf_symbol_suffix + "UTILONEUS','Uncle James','EQ:','US>',2,1,8,'USD'), "+\
    "('" + portf_symbol_suffix + "FINONEUS','Piggy Bank','EQ:','US>',2,1,9,'USD'), "+\
    "('" + portf_symbol_suffix + "MATONEUS','Iron String','EQ:','US>',2,1,10,'USD'), "+\
    "('" + portf_symbol_suffix + "TONEUS','Snail','BD:','US>',2,1,11,'USD'), "+\
    "('" + portf_symbol_suffix + "CSONEUS','Bread and Milk','EQ:','US>',2,1,12,'USD'), "+\
    "('" + portf_symbol_suffix + "NRGONEUS','The Fast and the Furious','EQ:','US>',2,1,13,'USD'), "+\
    "('" + portf_symbol_suffix + "TELCONEUS','The Phone Booth','EQ:','US>',2,1,14,'USD'), "+\
    "('" + portf_symbol_suffix + "REITONEUS','House of Cards','EQ:','US>',2,1,15,'USD'), "+\
    "('" + portf_symbol_suffix + "FOODONEUS','Burritos','EQ:','US>',2,1,12,'USD'), "+\
    "('" + portf_symbol_suffix + "DEFONEUS','Guns and Roses','EQ:','US>',2,1,4,'USD'), "+\
    "('" + portf_symbol_suffix + "TOBACONEUS','Party don-t stop','EQ:','US>',2,1,12,'USD')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "INDXONE") )
    print( set_alloc(portf_symbol_suffix, "INDUONEUS") )
    print( set_alloc(portf_symbol_suffix, "TECHONEUS") )
    print( set_alloc(portf_symbol_suffix, "HCONEUS") )
    print( set_alloc(portf_symbol_suffix, "CDONEUS") )
    print( set_alloc(portf_symbol_suffix, "UTILONEUS") )
    print( set_alloc(portf_symbol_suffix, "FINONEUS") )
    print( set_alloc(portf_symbol_suffix, "MATONEUS") )
    print( set_alloc(portf_symbol_suffix, "TONEUS") )
    print( set_alloc(portf_symbol_suffix, "CSONEUS") )
    print( set_alloc(portf_symbol_suffix, "NRGONEUS") )
    print( set_alloc(portf_symbol_suffix, "TELCONEUS") )
    print( set_alloc(portf_symbol_suffix, "REITONEUS") )
    print( set_alloc(portf_symbol_suffix, "FOODONEUS") )
    print( set_alloc(portf_symbol_suffix, "DEFONEUS") )
    print( set_alloc(portf_symbol_suffix, "TOBACONEUS") )
    return ac


################################################################################
print(set_portf_fx() +": "+ os.path.basename(__file__) )
print(set_portf_crypto() +": "+ os.path.basename(__file__) )
print(set_portf_commo() +": "+ os.path.basename(__file__) )
print(set_portf_multi() +": "+ os.path.basename(__file__) )
print(set_portf_us() +": "+ os.path.basename(__file__) )
