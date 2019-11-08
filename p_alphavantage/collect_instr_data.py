""" Collect and insert price data for each instruments into the db. """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import alpha_vantage
import json
import sys
import os
import gc
import requests
import datetime
import time
from datetime import timedelta
import random
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import debug, SmartAlphaPath
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def collect_av_instr_data():
    """
    Collect and insert price for each instrument into the database.
    Args:
        None
    Returns:
        None
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.symbol, symbol_list.uid, symbol_list.alphavantage "+\
    "FROM symbol_list INNER JOIN instruments ON symbol_list.symbol = instruments.symbol "+\
    "WHERE symbol_list.alphavantage NOT LIKE '' AND disabled=0 "
    cursor.execute(sql)
    rs = cursor.fetchall()
    ### Alphavantage API ######################################################
    # Data seems to be not  completely updated for previous day
    # before next day European market open: API max call is 5 per minute.
    ##########################################################################
    api_key_1 = 'XWOJ8KDFY4TLNYF0'
    api_key_2 = 'QD7YF5M1XAQYSNUA'
    api_key_3 = 'SMOLNVP8JUAC2OZ7'
    api_key_4 = '7RSFBNLP7W9BEPIG'
    api_key_5 = '1P15BOIG0RPPX7RG'
    api_key_6 = 'KJNC2D7YA2ZXN9NZ'
    api_key_7 = 'XTGE142SB2HRLQUF'
    api_key_8 = '2IT441B5KMPVJABL'
    api_key_9 = '6R22VXMUH6YXS4EU'
    api_key_10 = '5A9IEEKVEV0UOSF5'
    api_key_11 = 'TVXOUAOXKT7WFYYO'
    api_key_12 = 'WMNYHOIPKY3PHGZ2'
    api_key_13 = 'YXODKAE9CLL51S3E'
    api_key_14 = '87IPWKXWR8KIH4A3'
    api_key_15 = '1PQK2WUY052WNX2P'
    api_key_16 = 'WFFCSODIGWTZ0ZKH'
    api_key_17 = 'R6R1BFEW0KCNQSOV'
    api_key_18 = 'NLOOUESWS0IPW574'
    api_key_19 = '2OCRP8COYY938MCV'
    api_key_20 = 'D8DOFBC31KYWCXZK'

    url = "https://www.alphavantage.co/query"
    ############################################################################
    dta = datetime.datetime.now() - timedelta(days=1)
    dtb = datetime.datetime.now() - timedelta(days=2)
    dtc = datetime.datetime.now() - timedelta(days=3)
    dtd = datetime.datetime.now() - timedelta(days=4)
    dte = datetime.datetime.now() - timedelta(days=5)
    dtf = datetime.datetime.now() - timedelta(days=6)
    dtg = datetime.datetime.now() - timedelta(days=7)

    dtsql_a = dta.strftime('%Y%m%d')
    dtjson_a = dta.strftime('%Y-%m-%d')
    dtsql_b = dtb.strftime('%Y%m%d')
    dtjson_b = dtb.strftime('%Y-%m-%d')
    dtsql_c = dtc.strftime('%Y%m%d')
    dtjson_c = dtc.strftime('%Y-%m-%d')
    dtsql_d = dtd.strftime('%Y%m%d')
    dtjson_d = dtd.strftime('%Y-%m-%d')
    dtsql_e = dte.strftime('%Y%m%d')
    dtjson_e = dte.strftime('%Y-%m-%d')
    dtsql_f = dtf.strftime('%Y%m%d')
    dtjson_f = dtf.strftime('%Y-%m-%d')
    dtsql_g = dtg.strftime('%Y%m%d')
    dtjson_g = dtg.strftime('%Y-%m-%d')

    for row in rs:
        s = row[0]
        avs = row[2]

        key = random.randint(1, 20)
        if key == 1:
            api_key = api_key_1
        if key == 2:
            api_key = api_key_2
        if key == 3:
            api_key = api_key_3
        if key == 4:
            api_key = api_key_4
        if key == 5:
            api_key = api_key_5
        if key == 6:
            api_key = api_key_6
        if key == 7:
            api_key = api_key_7
        if key == 8:
            api_key = api_key_8
        if key == 9:
            api_key = api_key_9
        if key == 10:
            api_key = api_key_10
        if key == 11:
            api_key = api_key_11
        if key == 12:
            api_key = api_key_12
        if key == 13:
            api_key = api_key_13
        if key == 14:
            api_key = api_key_14
        if key == 15:
            api_key = api_key_15
        if key == 16:
            api_key = api_key_16
        if key == 17:
            api_key = api_key_17
        if key == 18:
            api_key = api_key_18
        if key == 19:
            api_key = api_key_19
        if key == 20:
            api_key = api_key_20
        debug(api_key)

        debug(s+": "+ os.path.basename(__file__))
        time.sleep(2)
        data = {"function": "TIME_SERIES_DAILY",
                "symbol": avs,
                "datatype": "json",
                "apikey": api_key}
        response = requests.get(url, data)
        data = response.json()
        debug(data)
        error_a = 0; error_b = 0; error_c = 0; error_d = 0; error_e = 0; error_f = 0; error_g = 0
        try:
            a = (data['Time Series (Daily)'][dtjson_a])
        except:
            error_a = 1
            pass
        try:
            b = (data['Time Series (Daily)'][dtjson_b])
        except:
            error_b = 1
            pass
        try:
            c = (data['Time Series (Daily)'][dtjson_c])
        except:
            error_c = 1
            pass
        try:
            d = (data['Time Series (Daily)'][dtjson_d])
        except:
            error_d = 1
            pass
        try:
            e = (data['Time Series (Daily)'][dtjson_e])
        except:
            error_e = 1
            pass
        try:
            f = (data['Time Series (Daily)'][dtjson_f])
        except:
            error_f = 1
            pass
        try:
            g = (data['Time Series (Daily)'][dtjson_g])
        except:
            error_g = 1
            pass

        pc_a = -1;
        pc_b = -1;
        pc_c = -1;
        pc_d = -1;
        pc_e = -1;
        pc_f = -1;
        pc_g = -1

        try:
            if error_a == 0:
                pc_a = a['4. close']
        except:
            pass
        try:
            if error_b == 0:
                pc_b = b['4. close']
        except:
            pass
        try:
            if error_c == 0:
                pc_c = c['4. close']
        except:
            pass
        try:
            if error_d == 0:
                pc_d = d['4. close']
        except:
            pass
        try:
            if error_e == 0:
                pc_e = e['4. close']
        except:
            pass
        try:
            if error_f == 0:
                pc_f = f['4. close']
        except:
            pass
        try:
            if error_g == 0:
                pc_g = g['4. close']
        except:
            pass

        cr_i = connection.cursor(pymysql.cursors.SSCursor)

        try:
            if pc_a != -1:
                sql_i = "INSERT IGNORE INTO price_instruments_data"+\
                "(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_a +"','"+str(pc_a)+"')"
                debug(sql_i)
                cr_i.execute(sql_i)
        except: pass
        try:
            if pc_b != -1:
                sql_i = "INSERT IGNORE INTO price_instruments_data"+\
                "(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_b +"','"+str(pc_b)+"')"
                debug(sql_i)
                cr_i.execute(sql_i)
        except: pass
        try:
            if pc_c != -1:
                sql_i = "INSERT IGNORE INTO price_instruments_data"+\
                "(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_c +"','"+str(pc_c)+"')"
                debug(sql_i)
                cr_i.execute(sql_i)
        except: pass
        try:
            if pc_d != -1:
                sql_i = "INSERT IGNORE INTO price_instruments_data"+\
                "(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_d +"','"+str(pc_d)+"')"
                debug(sql_i)
                cr_i.execute(sql_i)
        except: pass
        try:
            if pc_e != -1:
                sql_i = "INSERT IGNORE INTO price_instruments_data"+\
                "(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_e +"','"+str(pc_e)+"')"
                debug(sql_i)
                cr_i.execute(sql_i)
        except: pass
        try:
            if pc_f != -1:
                sql_i = "INSERT IGNORE INTO price_instruments_data"+\
                "(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_f +"','"+str(pc_f)+"')"
                debug(sql_i)
                cr_i.execute(sql_i)
        except: pass
        try:
            if pc_g != -1:
                sql_i = "INSERT IGNORE INTO price_instruments_data"+\
                "(symbol, date, price_close) VALUES ('"+s+"','"+ dtsql_g +"','"+str(pc_g)+"')"
                debug(sql_i)
                cr_i.execute(sql_i)
        except: pass

        connection.commit()
        gc.collect()
        cr_i.close()
    cursor.close()

collect_av_instr_data()
