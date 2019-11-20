""" Insert Oanda price from collection thru csv download """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import time
import csv
from pathlib import Path
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_core()))
from sa_logging import log_this
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()



def insert_db_price_data():
    """
    Collect and import instruments price data from Oanda into the database
    Args:
        None
    Returns:
        None
    """
    log_this('1. oanda_insert_db_price_data', 0)
    csvdir = SETT.get_path_r_oanda_src()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol, uid FROM symbol_list WHERE oanda<>'' "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        symbol = row[0]
        uid = row[1]
        file_str = csvdir+str(uid)+'.csv'
        filepath = Path(file_str)
        if filepath.exists():
            with open(file_str) as csvfile:
                csv_file = csv.reader(csvfile, delimiter=',')
                i = 0
                inserted_values = ''
                for row in csv_file:
                    time.sleep(0.2)
                    price_date = row[0]
                    price_date = price_date.replace('.', '-')
                    price_date = price_date.replace('X', '')
                    price_date = price_date.replace('-', '')
                    price_date = '%.8s' % price_date
                    price_close = row[1]
                    if price_close != "NA" and i > 0:
                        if i == 1:
                            sep = ''
                        else:
                            sep = ','
                        inserted_values = inserted_values + sep +\
                        "('"+symbol+"',"+price_date+","+price_close+")"
                        debug(symbol +": "+ os.path.basename(__file__) + " - " + inserted_values)
                    i += 1
                cr_q_ins = connection.cursor(pymysql.cursors.SSCursor)
                sql_q_ins = "INSERT IGNORE INTO price_instruments_data "+\
                "(symbol, date, price_close) VALUES " + inserted_values
                cr_q_ins.execute(sql_q_ins)
                connection.commit()
                cr_q_ins.close()
    cursor.close()
    connection.close()
    log_this('1. oanda_insert_db_price_data', 1)

insert_db_price_data()
