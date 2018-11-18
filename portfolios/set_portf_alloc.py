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

def set_alloc(sfx,s):
    symbol = sfx + s

    if (symbol == sfx+"FXONE" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "FXONE','EURUSD',10000),"+\
        "('" + sfx + "FXONE','GBPUSD',10000),"+\
        "('" + sfx + "FXONE','EURGBP',10000)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"CRYPTONE" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "CRYPTONE','BITCOIN',1),"+\
        "('" + sfx + "CRYPTONE','ETHEREUM',1),"+\
        "('" + sfx + "CRYPTONE','RIPPLE',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"INDXONE" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "INDXONE','SPX',1),"+\
        "('" + sfx + "INDXONE','INDEXFTSE:UKX',1),"+\
        "('" + sfx + "INDXONE','INDEXDB:DAX',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"INDUONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "INDUONEUS','NYSE:FDX',1),"+\
        "('" + sfx + "INDUONEUS','NYSE:MMM',1),"+\
        "('" + sfx + "INDUONEUS','NYSE:UPS',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"TECHONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "TECHONEUS','NASDAQ:FB',1),"+\
        "('" + sfx + "TECHONEUS','NASDAQ:AMZN',1),"+\
        "('" + sfx + "TECHONEUS','NASDAQ:GOOG',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"HCONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "HCONEUS','NASDAQ:AMGN',1),"+\
        "('" + sfx + "HCONEUS','NASDAQ:GILD',1),"+\
        "('" + sfx + "HCONEUS','NYSE:CI',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"CDONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "CDONEUS','NASDAQ:FOXA',1),"+\
        "('" + sfx + "CDONEUS','NASDAQ:MAR',1),"+\
        "('" + sfx + "CDONEUS','NASAQ:SBUX',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"UTILONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "UTILONEUS','NYSE:D',1),"+\
        "('" + sfx + "UTILONEUS','NYSE:EXC',1),"+\
        "('" + sfx + "UTILONEUS','NYSE:ED',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"FINONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "FINONEUS','NYSE:BAC',1),"+\
        "('" + sfx + "FINONEUS','NYSE:GS',1),"+\
        "('" + sfx + "FINONEUS','NYSE:JPM',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"MATONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "MATONEUS','NYSE:NUE',1),"+\
        "('" + sfx + "MATONEUS','NYSE:AA',1),"+\
        "('" + sfx + "MATONEUS','NYSE:X',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"TONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "TONEUS','NASDAQ:TLT',1),"+\
        "('" + sfx + "TONEUS','GLD',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"CSONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "CSONEUS','NYSE:PG',1),"+\
        "('" + sfx + "CSONEUS','NYSE:WMT',1),"+\
        "('" + sfx + "CSONEUS','NYSE:KO',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"NRGONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "NRGONEUS','NYSE:NBL',1),"+\
        "('" + sfx + "NRGONEUS','NYSE:CVX',1),"+\
        "('" + sfx + "NRGONEUS','NYSE:PSX',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"TELCONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "TELCONEUS','NYSE:VZ',1),"+\
        "('" + sfx + "TELCONEUS','NYSE:T',1),"+\
        "('" + sfx + "TELCONEUS','NYSE:S',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"REITONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "REITONEUS','NYSEARCA:XLRE',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"COMMONE" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "COMMONE','GLD',1),"+\
        "('" + sfx + "COMMONE','USO',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"FOODONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "FOODONEUS','NYSE:DRI',1),"+\
        "('" + sfx + "FOODONEUS','NYSE:MCD',1),"+\
        "('" + sfx + "FOODONEUS','NYSE:CMG',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"MULTIONE" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "MULTIONE','NYSE:PG',1),"+\
        "('" + sfx + "MULTIONE','NASDAQ:AMD',1),"+\
        "('" + sfx + "MULTIONE','BITCOIN',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"GOJONE" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "GOJONE','GLD',1),"+\
        "('" + sfx + "GOJONE','USDJPY',1),"+\
        "('" + sfx + "GOJONE','EURJPY',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"DEFONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "DEFONEUS','NYSE:LMT',1),"+\
        "('" + sfx + "DEFONEUS','NYSE:BA',1),"+\
        "('" + sfx + "DEFONEUS','NASDAQ:FLIR',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    if (symbol == sfx+"TOBACONEUS" ):
        sql = "INSERT INTO portfolios(portf_symbol, symbol, quantity) VALUES "+\
        "('" + sfx + "TOBACONEUS','NYSE:MO',1),"+\
        "('" + sfx + "TOBACONEUS','NYSE:PM',1)"
        try:
            cr.execute(sql)
            connection.commit()
        except Exception as e: print(e)

    ##############
    return symbol
