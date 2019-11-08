# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cr = connection.cursor(pymysql.cursors.SSCursor)

sql = "DELETE FROM portfolios"
cr.execute(sql)
connection.commit()
cr.close()

def set_alloc(sfx,s):
    symbol = sfx + s

    cr = connection.cursor(pymysql.cursors.SSCursor)

################################################################################
    if (symbol == sfx+"FXONE" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "FXONE','EURUSD',1,'long/short','neutral'),"+\
        "('" + sfx + "FXONE','GBPUSD',1,'long/short','neutral'),"+\
        "('" + sfx + "FXONE','EURGBP',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"CRYPTONE" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "CRYPTONE','BITCOIN',1,'long/short','neutral'),"+\
        "('" + sfx + "CRYPTONE','ETHEREUM',1,'long/short','neutral'),"+\
        "('" + sfx + "CRYPTONE','RIPPLE',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"INDXONE" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "INDXONE','SPX',1,'long/short','neutral'),"+\
        "('" + sfx + "INDXONE','INDEXFTSE:UKX',1,'long/short','neutral'),"+\
        "('" + sfx + "INDXONE','INDEXDB:DAX',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"INDUONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "INDUONEUS','NYSE:FDX',1,'long/short','neutral'),"+\
        "('" + sfx + "INDUONEUS','NYSE:MMM',1,'long/short','neutral'),"+\
        "('" + sfx + "INDUONEUS','NYSE:UPS',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"TECHONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "TECHONEUS','NASDAQ:FB',1,'long/short','neutral'),"+\
        "('" + sfx + "TECHONEUS','NASDAQ:AMZN',1,'long/short','neutral'),"+\
        "('" + sfx + "TECHONEUS','NASDAQ:GOOG',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"HCONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "HCONEUS','NASDAQ:AMGN',1,'long/short','neutral'),"+\
        "('" + sfx + "HCONEUS','NASDAQ:GILD',1,'long/short','neutral'),"+\
        "('" + sfx + "HCONEUS','NYSE:CI',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"CDONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "CDONEUS','NASDAQ:FOXA',1,'long/short','neutral'),"+\
        "('" + sfx + "CDONEUS','NASDAQ:MAR',1,'long/short','neutral'),"+\
        "('" + sfx + "CDONEUS','NASDAQ:SBUX',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"UTILONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "UTILONEUS','NYSE:D',1,'long/short','neutral'),"+\
        "('" + sfx + "UTILONEUS','NYSE:EXC',1,'long/short','neutral'),"+\
        "('" + sfx + "UTILONEUS','NYSE:ED',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"FINONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "FINONEUS','NYSE:BAC',1,'long/short','neutral'),"+\
        "('" + sfx + "FINONEUS','NYSE:GS',1,'long/short','neutral'),"+\
        "('" + sfx + "FINONEUS','NYSE:JPM',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"MATONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "MATONEUS','NYSE:NUE',1,'long/short','neutral'),"+\
        "('" + sfx + "MATONEUS','NYSE:AA',1,'long/short','neutral'),"+\
        "('" + sfx + "MATONEUS','NYSE:X',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"TONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "TONEUS','NASDAQ:TLT',1,'long/short','neutral'),"+\
        "('" + sfx + "TONEUS','GLD',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"CSONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "CSONEUS','NYSE:PG',1,'long/short','neutral'),"+\
        "('" + sfx + "CSONEUS','NYSE:WMT',1,'long/short','neutral'),"+\
        "('" + sfx + "CSONEUS','NYSE:KO',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"NRGONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "NRGONEUS','NYSE:NBL',1,'long/short','neutral'),"+\
        "('" + sfx + "NRGONEUS','NYSE:CVX',1,'long/short','neutral'),"+\
        "('" + sfx + "NRGONEUS','NYSE:PSX',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"TELCONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "TELCONEUS','NYSE:VZ',1,'long/short','neutral'),"+\
        "('" + sfx + "TELCONEUS','NYSE:T',1,'long/short','neutral'),"+\
        "('" + sfx + "TELCONEUS','NYSE:S',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"REITONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "REITONEUS','NYSEARCA:XLRE',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"COMMONE" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "COMMONE','GLD',1,'long/short','neutral'),"+\
        "('" + sfx + "COMMONE','USO',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"FOODONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "FOODONEUS','NYSE:DRI',1,'long/short','neutral'),"+\
        "('" + sfx + "FOODONEUS','NYSE:MCD',1,'long/short','neutral'),"+\
        "('" + sfx + "FOODONEUS','NYSE:CMG',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"MULTIONE" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "MULTIONE','NYSE:PG',1,'long/short','neutral'),"+\
        "('" + sfx + "MULTIONE','NASDAQ:AMD',1,'long/short','neutral'),"+\
        "('" + sfx + "MULTIONE','BITCOIN',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"GOJONE" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "GOJONE','GLD',1,'long/short','neutral'),"+\
        "('" + sfx + "GOJONE','USDJPY',1,'long/short','neutral'),"+\
        "('" + sfx + "GOJONE','EURJPY',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"DEFONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "DEFONEUS','NYSE:LMT',1,'long/short','neutral'),"+\
        "('" + sfx + "DEFONEUS','NYSE:BA',1,'long/short','neutral'),"+\
        "('" + sfx + "DEFONEUS','NASDAQ:FLIR',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

################################################################################
    if (symbol == sfx+"TOBACONEUS" ):
        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('" + sfx + "TOBACONEUS','NYSE:MO',1,'long/short','neutral'),"+\
        "('" + sfx + "TOBACONEUS','NYSE:PM',1,'long/short','neutral')"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: debug(e)
################################################################################

    cr.close()
    ##############
    return symbol
