# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
from ta_main_update_data import *

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

sys.path.append(os.path.abspath( sett.get_path_core() ))

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()
import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def recalc_histdata(symbol):
    try:
        get_update_instr_data(1,True,symbol)

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'UPDATE price_instruments_data SET is_ta_calc=0 WHERE symbol = "'+ str(symbol) +'"'
        cr.execute(sql)
        connection.commit()
        cr.close()
        connection.close()
        get_update_instr_data(1,True,symbol)
        print(str(symbol) + ': Done.')

    except Exception as e: print(e)

print("###############################################################################")
print("Recalculate historical data for specific function")
print("-------------------------------------------------")
print("IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT")
print("recalc_histdata(symbol)")
print(" ")
print("provide the following parameters:")
print("(1) symbol")
print("--------------------------------------")
print("Affected tables/column:")
print("-----------------------")
print("1. price_instruments_data.*")
print("###############################################################################")
recalc_histdata('EURHUF')
recalc_histdata('GBPHUF')
recalc_histdata('CHFHUF')
recalc_histdata('USDPLN')
recalc_histdata('NASDAQ:AAXJ')
recalc_histdata('NASDAQ:ACWI')
recalc_histdata('NYSEARCA:AGG')
recalc_histdata('NYSEARCA:AMLP')
recalc_histdata('NYSEARCA:AOA')
recalc_histdata('NYSEARCA:AOK')
recalc_histdata('NYSEARCA:AOR')
recalc_histdata('NYSEARCA:ASHR')
recalc_histdata('NYSEARCA:BIL')
recalc_histdata('NYSEARCA:BKLN')
recalc_histdata('NASDAQ:BND')
recalc_histdata('NYSEARCA:BOND')
recalc_histdata('NYSEARCA:BSV')
recalc_histdata('NYSEARCA:CORN')
recalc_histdata('NYSEARCA:DBA')
recalc_histdata('NYSEARCA:DGRO')
recalc_histdata('NYSEARCA:DIA')
recalc_histdata('NYSEARCA:EEM')
recalc_histdata('NYSEARCA:EFA')
recalc_histdata('NASDAQ:EMB')
recalc_histdata('NYSEARCA:EWG')
recalc_histdata('NYSEARCA:EWH')
recalc_histdata('NYSEARCA:EWJ')
recalc_histdata('NYSEARCA:EWT')
recalc_histdata('NYSEARCA:EWW')
recalc_histdata('NYSEARCA:EWY')
recalc_histdata('NYSEARCA:EWZ')
