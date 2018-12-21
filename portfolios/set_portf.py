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
connection.commit()
sql = "DELETE FROM symbol_list WHERE symbol LIKE '"+ portf_symbol_suffix +"%' "
cr.execute(sql)
connection.commit()
sql = "DELETE FROM chart_data WHERE symbol LIKE '"+ portf_symbol_suffix +"%' "
cr.execute(sql)
connection.commit()
sql = "DELETE FROM feed WHERE symbol LIKE '%"+ portf_symbol_suffix +"%' "
cr.execute(sql)
connection.commit()

cr.close()



'''
### Template description for portfolio:

01) This portfolio includes assets in the "..." industry.
02) This is a quantamental portfolio trading on some of the most lucrative financial assets, cryptos and fx.
03) Selected from a range of dynamic metrics, the selected assests are the most desirable in the "..." industry.
04) A simple yet highly vetted long/short portfolio of three financial instruments in the "..." industry.
05) The specified portfolio aims to provide an absolute return of "...%" in the next 7 days.
06) With an exposure in the "..." industry, the defined porfolio projects an absolute positive return in the next couple days.
07) A combination of assets from different industries statistically selected to provide positive gains over the next week.
08) Three assets scanned through the "..." industry, with a focus to achieve the most preferable gains in less than 7 days.
09) A playsafe portfolio, involving only long positions of financial assets in the "..." industry.
10) Short selling portfolio targetting bearish moves in "..." industry, trading three selected assets.
11) This portfolio trades on "..." industry, having a combination of 3 financial instruments carefully selected.

'''

################################################################################
# Forex Portfolio
################################################################################
def set_portf_fx():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "fx"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE','No-Fly Zone Airspace','FX:','GO>',5,10000,1,'USD','With an exposure in the foreign exchange market, the defined porfolio projects an absolute positive return in the next couple days.')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "FXONE") )
    cr.close()
    return ac

################################################################################
# Crypto Portfolio
################################################################################
def set_portf_crypto():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "crypto"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE','The Hot Potato','CR:','GO>',5,1,2,'USD','This is a quantamental portfolio trading on some of the most lucrative financial assets, the portfolio consists of a long/short strategy on most popular cryptocurrencies.')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "CRYPTONE") )
    cr.close()
    return ac

################################################################################
# Commodities Portfolio
################################################################################
def set_portf_commo():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "commo"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE','Gold Digger','CO:','GO>',2,1,18,'USD','This portfolio includes two of the most traded commodities products.')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "COMMONE") )
    cr.close()
    return ac

################################################################################
# Multi-Asset Portfolio
################################################################################
def set_portf_multi():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "multi"
    sql = "INSERT INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE'), "+\
    "('" + portf_symbol_suffix + "GOJONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE','Milkshake','MA:','GO>',5,1,19,'USD','This is a quantamental portfolio trading on some of the most lucrative financial assets, a combination of relevant stocks and cryptocurrencies.'), "+\
    "('" + portf_symbol_suffix + "GOJONE','Safe Haven','MA:','GO>',5,1,19,'USD','This is a playsafe portfolio, involving only Gold ETF and Japanese Yen.')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
    print( set_alloc(portf_symbol_suffix, "MULTIONE") )
    print( set_alloc(portf_symbol_suffix, "GOJONE") )
    cr.close()
    return ac

################################################################################
# US Equity Portfolio
################################################################################
def set_portf_us():
    cr = connection.cursor(pymysql.cursors.SSCursor)
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
    sql = "INSERT INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description) VALUES "+\
    "('" + portf_symbol_suffix + "INDXONE','The Escalator','EQ:','GO>',2,1,17,'USD','This portfolio includes carefully selected world major indices traded with a long/short strategy.'), "+\
    "('" + portf_symbol_suffix + "INDUONEUS','Smoke Up','EQ:','US>',2,1,4,'USD','This portfolio is a combination of assets from different industries statistically selected to provide positive gains over the next week.'), "+\
    "('" + portf_symbol_suffix + "TECHONEUS','Time Travel','EQ:','US>',2,1,5,'USD','A simple yet highly vetted long/short portfolio of three US equities in the Tech industry.'), "+\
    "('" + portf_symbol_suffix + "HCONEUS','Dr Kam','EQ:','US>',2,1,6,'USD','This portfolio of three assets scanned through the healthcare industry, with a focus to achieve the most preferable gains in less than 7 days.'), "+\
    "('" + portf_symbol_suffix + "CDONEUS','Rich Kids','EQ:','US>',2,1,7,'USD','With an exposure in three major US equities in the consumer discretionary sector, the defined porfolio projects an absolute positive return in the next couple days.'), "+\
    "('" + portf_symbol_suffix + "UTILONEUS','Uncle James','EQ:','US>',2,1,8,'USD','This portfolio trades on US utilities sector, having a combination of 3 financial instruments carefully selected.'), "+\
    "('" + portf_symbol_suffix + "FINONEUS','Piggy Bank','EQ:','US>',2,1,9,'USD','Selected from a range of dynamic metrics, the selected assests are the most desirable in the finance and banking industry.'), "+\
    "('" + portf_symbol_suffix + "MATONEUS','Iron String','EQ:','US>',2,1,10,'USD','This portfolio includes assets in the US materials sector.'), "+\
    "('" + portf_symbol_suffix + "TONEUS','Snail','BD:','US>',2,1,11,'USD','With an exposure in the US Treasury bonds and Gold ETF, the defined porfolio projects an absolute positive return in the next couple days.'), "+\
    "('" + portf_symbol_suffix + "CSONEUS','Bread and Milk','EQ:','US>',2,1,12,'USD','A simple yet highly vetted long/short portfolio of three financial instruments in the consumer staples sector.'), "+\
    "('" + portf_symbol_suffix + "NRGONEUS','The Fast and the Furious','EQ:','US>',2,1,13,'USD','Selected from a range of dynamic metrics, the selected three assests are the most desirable in the energy sector to provide positive gains from a long/short strategy in the next couple of days.'), "+\
    "('" + portf_symbol_suffix + "TELCONEUS','The Phone Booth','EQ:','US>',2,1,14,'USD','With an exposure in the telecommunications sector industry with 3 selected US equities, the defined porfolio projects an absolute positive return in the next couple days.'), "+\
    "('" + portf_symbol_suffix + "REITONEUS','House of Cards','EQ:','US>',2,1,15,'USD','With an exposure in the real estate development industry, the defined porfolio projects an absolute positive return in the next couple days.'), "+\
    "('" + portf_symbol_suffix + "FOODONEUS','Burritos','EQ:','US>',2,1,12,'USD','This portfolio trades on food and beverage sector, having a combination of 3 financial instruments carefully selected.'), "+\
    "('" + portf_symbol_suffix + "DEFONEUS','Guns and Roses','EQ:','US>',2,1,4,'USD','This portfolio includes carefully selected three US stocks in the defense sector traded with a long/short strategy.'), "+\
    "('" + portf_symbol_suffix + "TOBACONEUS','Party don-t stop','EQ:','US>',2,1,12,'USD','This portfolio with just 3 US equities in the tobacco and beverage sector not just only beat the consumer staples sector, but beat the sh*t out of you.')"
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
    cr.close()
    return ac


################################################################################
print(set_portf_fx() +": "+ os.path.basename(__file__) )
print(set_portf_crypto() +": "+ os.path.basename(__file__) )
print(set_portf_commo() +": "+ os.path.basename(__file__) )
print(set_portf_multi() +": "+ os.path.basename(__file__) )
print(set_portf_us() +": "+ os.path.basename(__file__) )
