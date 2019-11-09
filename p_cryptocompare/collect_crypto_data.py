""" Collect and insert Cryptocurrency price data into the database """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import urllib.request
import json
import sys
import os
from datetime import datetime
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_portf_suffix
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


import pymysql.cursors

def collect_crypto_data():
    """
    Collect and import crypto price data into the database
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
    sql = "SELECT symbol_list.symbol, symbol_list.uid, symbol_list.fsym, symbol_list.tsym "+\
    "FROM symbol_list INNER JOIN instruments ON "+\
    "symbol_list.symbol = instruments.symbol WHERE symbol_list.symbol "+\
    "NOT LIKE '%"+ get_portf_suffix() +"%' AND instruments.asset_class = 'CR:' AND disabled =0"
    cursor.execute(sql)
    res = cursor.fetchall()
    i = 1
    for row in res:
        symbol = row[0]
        fsym = row[2]
        tsym = row[3]

        debug(symbol+": "+ os.path.basename(__file__))

        ### Cryptocompare API ######################################################
        url = "https://min-api.cryptocompare.com/data/histoday?"+\
        "fsym="+fsym+"&tsym="+tsym+"&limit=30&aggregate=1&e=CCCAGG"
        ############################################################################

        request = urllib.request.Request(url)
        opener = urllib.request.build_opener()

        fil = opener.open(request)
        j = json.loads(fil.read())
        k = len(j['Data'])
        i = 1
        inserted_values = ''
        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        while i < k:
            price_close = j['Data'][i]['close']
            date = j['Data'][i]['time']
            date_today = datetime.utcfromtimestamp(int(date))
            if i == 1:
                sep = ''
            else:
                sep = ','
            inserted_values = inserted_values + sep +\
            "('"+symbol+"','"+date_today.strftime('%Y%m%d')+"','"+str(price_close)+"')"
            debug(inserted_values)
            i += 1
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES " +\
        inserted_values
        cr_i.execute(sql_i)
        connection.commit()
        cr_i.close()
    cursor.close()

collect_crypto_data()
