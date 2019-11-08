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

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import SmartAlphaPath, debug
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import sa_db_access
access_obj = sa_db_access()
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()


import pymysql.cursors

def collect_crypto_data():
    """
    Collect and import crypto price data into the database
    Args:
        None
    Returns:
        None
    """    
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol_list.symbol, symbol_list.uid, symbol_list.fsym, symbol_list.tsym "+\
    "FROM symbol_list INNER JOIN instruments ON "+\
    "symbol_list.symbol = instruments.symbol WHERE symbol_list.symbol "+\
    "NOT LIKE '%"+ get_portf_suffix() +"%' AND instruments.asset_class = 'CR:' AND disabled =0"
    cursor.execute(sql)
    rs = cursor.fetchall()
    i = 1
    for row in rs:
        s = row[0]
        uid = row[1]
        fsym = row[2]
        tsym = row[3]
    
        debug(s+": "+ os.path.basename(__file__) )
    
        ### Cryptocompare API ######################################################
        url = "https://min-api.cryptocompare.com/data/histoday?"+\
        "fsym="+fsym+"&tsym="+tsym+"&limit=30&aggregate=1&e=CCCAGG"
        ############################################################################
    
        request = urllib.request.Request(url)
        opener = urllib.request.build_opener()
        response = opener.open(request)
    
        f = opener.open(request)
        j = json.loads(f.read())
        k = len(j['Data'])
        i= 1
        inserted_values = ''
        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        while i<k:
            pc = j['Data'][i]['close']
            d = j['Data'][i]['time']
            dt = datetime.utcfromtimestamp(int(d))
            if i == 1:
                sep = ''
            else:
                sep = ','
            inserted_values = inserted_values + sep + "('"+s+"','"+dt.strftime('%Y%m%d')+"','"+str(pc)+"')"
            debug(inserted_values)
            i += 1
        sql_i = "INSERT IGNORE INTO price_instruments_data(symbol, date, price_close) VALUES " + inserted_values
        cr_i.execute(sql_i)
        connection.commit()
        cr_i.close()
    cursor.close()
    
collect_crypto_data()

