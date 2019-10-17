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

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

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


def get_user_smartalpha_id():

    sa_bot_nickname = 'smartalpha'
    r = ''
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT id FROM users WHERE nickname = '"+ sa_bot_nickname +"'"
        cr.execute('SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;')
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
        cr.close()
    except Exception as e: debug(e)
    return r
owner_sa_bot_id = get_user_smartalpha_id()

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
    sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
    "('" + portf_symbol_suffix + "FXONE','No-Fly Global Forex long/short','FX:','GO>',5,1,1,'USD','With an exposure in the foreign exchange market, the defined porfolio projects an absolute positive return in the next couple days.',1000,"+ str(owner_sa_bot_id) +")"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    debug( set_alloc(portf_symbol_suffix, "FXONE") )
    cr.close()
    return ac

################################################################################
# Crypto Portfolio
################################################################################
def set_portf_crypto():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "crypto"
    sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
    "('" + portf_symbol_suffix + "CRYPTONE','The Hot Potato Global Crypto long/short','CR:','GO>',5,1,2,'USD','This is a quantamental portfolio trading on some of the most lucrative financial assets, the portfolio consists of a long/short strategy on most popular cryptocurrencies.',1000,"+ str(owner_sa_bot_id) +")"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    debug( set_alloc(portf_symbol_suffix, "CRYPTONE") )
    cr.close()
    return ac

################################################################################
# Commodities Portfolio
################################################################################
def set_portf_commo():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "commo"
    sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
    "('" + portf_symbol_suffix + "COMMONE','Gold Digger Global Commodities long/short','CO:','GO>',2,1,18,'USD','This portfolio includes two of the most traded commodities products.',1000,"+ str(owner_sa_bot_id) +")"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    debug( set_alloc(portf_symbol_suffix, "COMMONE") )
    cr.close()
    return ac

################################################################################
# Multi-Asset Portfolio
################################################################################
def set_portf_multi():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "multi"
    sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE'), "+\
    "('" + portf_symbol_suffix + "GOJONE')"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
    "('" + portf_symbol_suffix + "MULTIONE','Milkshake Global Multi-asset long/short','MA:','GO>',5,1,19,'USD','This is a quantamental portfolio trading on some of the most lucrative financial assets, a combination of relevant stocks and cryptocurrencies.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "GOJONE','Safe Haven Global Multi-asset long/short','MA:','GO>',5,1,19,'USD','This is a playsafe portfolio, involving only Gold ETF and Japanese Yen.',1000,"+ str(owner_sa_bot_id) +")"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    debug( set_alloc(portf_symbol_suffix, "MULTIONE") )
    debug( set_alloc(portf_symbol_suffix, "GOJONE") )
    cr.close()
    return ac

################################################################################
# US Equity Portfolio
################################################################################
def set_portf_us():
    cr = connection.cursor(pymysql.cursors.SSCursor)
    ac = "us"
    sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
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
    except Exception as e: debug(e)
    sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
    "('" + portf_symbol_suffix + "INDXONE','The Escalator Global Equity long/short','EQ:','GO>',2,1,17,'USD','This portfolio includes carefully selected world major indices traded with a long/short strategy.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "INDUONEUS','Smoke Up U.S. Equity long/short','EQ:','US>',2,1,4,'USD','This portfolio is a combination of assets from different industries statistically selected to provide positive gains over the next week.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "TECHONEUS','Time Travel U.S. Equity long/short','EQ:','US>',2,1,5,'USD','A simple yet highly vetted long/short portfolio of three US equities in the Tech industry.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "HCONEUS','Nip Tuck U.S. Equity long/short','EQ:','US>',2,1,6,'USD','This portfolio of three assets scanned through the healthcare industry, with a focus to achieve the most preferable gains in less than 7 days.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "CDONEUS','Rich Kids U.S. Equity long/short','EQ:','US>',2,1,7,'USD','With an exposure in three major US equities in the consumer discretionary sector, the defined porfolio projects an absolute positive return in the next couple days.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "UTILONEUS','Uncle James U.S. Equity long/short','EQ:','US>',2,1,8,'USD','This portfolio trades on US utilities sector, having a combination of 3 financial instruments carefully selected.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "FINONEUS','Piggy Bank U.S. Equity long/short','EQ:','US>',2,1,9,'USD','Selected from a range of dynamic metrics, the selected assests are the most desirable in the finance and banking industry.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "MATONEUS','Iron String U.S. Equity long/short','EQ:','US>',2,1,10,'USD','This portfolio includes assets in the US materials sector.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "TONEUS','Snail U.S. Bonds long/short','BD:','US>',2,1,11,'USD','With an exposure in the US Treasury bonds and Gold ETF, the defined porfolio projects an absolute positive return in the next couple days.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "CSONEUS','Bread and Milk U.S. Equity long/short','EQ:','US>',2,1,12,'USD','A simple yet highly vetted long/short portfolio of three financial instruments in the consumer staples sector.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "NRGONEUS','The Fast and Furious U.S. Equity long/short','EQ:','US>',2,1,13,'USD','Selected from a range of dynamic metrics, the selected three assests are the most desirable in the energy sector to provide positive gains from a long/short strategy in the next couple of days.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "TELCONEUS','The Phone Booth U.S. Equity long/short','EQ:','US>',2,1,14,'USD','With an exposure in the telecommunications sector industry with 3 selected US equities, the defined porfolio projects an absolute positive return in the next couple days.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "REITONEUS','House of Cards U.S. Equity long/short','EQ:','US>',2,1,15,'USD','With an exposure in the real estate development industry, the defined porfolio projects an absolute positive return in the next couple days.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "FOODONEUS','Burritos U.S. Equity long/short','EQ:','US>',2,1,12,'USD','This portfolio trades on food and beverage sector, having a combination of 3 financial instruments carefully selected.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "DEFONEUS','Guns and Roses U.S. Equity long/short','EQ:','US>',2,1,4,'USD','This portfolio includes carefully selected three US stocks in the defense sector traded with a long/short strategy.',1000,"+ str(owner_sa_bot_id) +"), "+\
    "('" + portf_symbol_suffix + "TOBACONEUS','Party don-t stop U.S. Equity long/short','EQ:','US>',2,1,12,'USD','This portfolio with just 3 US equities in the tobacco and beverage sector not just only beat the consumer staples sector, but beat the sh*t out of you.',1000,"+ str(owner_sa_bot_id) +")"
    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: debug(e)
    debug( set_alloc(portf_symbol_suffix, "INDXONE") )
    debug( set_alloc(portf_symbol_suffix, "INDUONEUS") )
    debug( set_alloc(portf_symbol_suffix, "TECHONEUS") )
    debug( set_alloc(portf_symbol_suffix, "HCONEUS") )
    debug( set_alloc(portf_symbol_suffix, "CDONEUS") )
    debug( set_alloc(portf_symbol_suffix, "UTILONEUS") )
    debug( set_alloc(portf_symbol_suffix, "FINONEUS") )
    debug( set_alloc(portf_symbol_suffix, "MATONEUS") )
    debug( set_alloc(portf_symbol_suffix, "TONEUS") )
    debug( set_alloc(portf_symbol_suffix, "CSONEUS") )
    debug( set_alloc(portf_symbol_suffix, "NRGONEUS") )
    debug( set_alloc(portf_symbol_suffix, "TELCONEUS") )
    debug( set_alloc(portf_symbol_suffix, "REITONEUS") )
    debug( set_alloc(portf_symbol_suffix, "FOODONEUS") )
    debug( set_alloc(portf_symbol_suffix, "DEFONEUS") )
    debug( set_alloc(portf_symbol_suffix, "TOBACONEUS") )
    cr.close()
    return ac


################################################################################
debug(set_portf_fx() +": "+ os.path.basename(__file__) )
debug(set_portf_crypto() +": "+ os.path.basename(__file__) )
debug(set_portf_commo() +": "+ os.path.basename(__file__) )
debug(set_portf_multi() +": "+ os.path.basename(__file__) )
debug(set_portf_us() +": "+ os.path.basename(__file__) )
