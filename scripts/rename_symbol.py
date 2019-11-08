# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import time
import datetime
from datetime import timedelta

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

sys.path.append(os.path.abspath( sett.get_path_core() ))
from ta_main_update_data import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def rename_symbol(current_symbol,new_symbol):
    try:
        rename_s_table('symbol_list',current_symbol,new_symbol)
        rename_s_table('instruments',current_symbol,new_symbol)
        rename_s_table('feed',current_symbol,new_symbol)
        rename_s_table('trades',current_symbol,new_symbol)
        rename_s_table('chart_data',current_symbol,new_symbol)
        rename_s_table('portfolios',current_symbol,new_symbol)
        rename_s_table('price_instruments_data',current_symbol,new_symbol)
        connection.close()
    except Exception as e: print(e)

def rename_s_table(table,current_s,new_s):
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'UPDATE '+ str(table) + ' SET symbol="'+ str(new_s) +'" WHERE symbol="'+ str(current_s) +'"'
        print(sql)
        cr.execute(sql)
        connection.commit()
        cr.close()
    except Exception as e: print(e)


print("###############################################################################")
print("Rename symbol function")
print("--------------------------------------")
print("IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT")
print("rename_symbol(current_symbol,new_symbol)")
print(" ")
print("provide the following parameters:")
print("(1) the current symbol")
print("(2) the new symbol to change to...")
print("--------------------------------------")
print("Affected tables/column:")
print("-----------------------")
print("1. symbol_list.symbol")
print("2. instruments.symbol")
print("3. feed.symbol")
print("4. trades.symbol")
print("5. chart_data.symbol")
print("6. portfolios.symbol")
print("7. price_instruments_data.symbol")
print("###############################################################################")
