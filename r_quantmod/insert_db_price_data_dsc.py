""" Import data collected with Quantmod csv output into database DESC """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import time
import gc
import csv
from pathlib import Path
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_core()))
from logging import log_this
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def insert_db_price_data_dsc():
    """
    Insert collected price data from Quantmod csv into database in
    descending order.
    Args:
        None
    Returns:
        None
    """
    log_this('1. quantmod_insert_db_price_data_dsc', 0)
    csvdir = SETT.get_path_r_quantmod_src()
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr_cnt = connection.cursor(pymysql.cursors.SSCursor)
    sql_cnt = "SELECT COUNT(*) FROM symbol_list"
    cr_cnt.execute(sql_cnt)
    rs_cnt = cr_cnt.fetchall()
    for row in rs_cnt:
        j = (((int(row[0]))/2)+10)
    cr_cnt.close()

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol, uid FROM symbol_list ORDER BY symbol DESC"
    cursor.execute(sql)
    res = cursor.fetchall()
    k = 1
    for row in res:
        if k <= j:
            uid = row[1]
            symbol = row[0]
            file_str = csvdir+str(uid)+'.csv'
            debug(str(uid) + ' - ' + str(symbol) + '------------------------------')
            filepath = Path(file_str)
            if filepath.exists():
                with open(file_str) as csvfile:
                    csv_file = csv.reader(csvfile, delimiter=',')
                    i = 1
                    inserted_values = ''
                    for row in csv_file:
                        time.sleep(0.2)
                        price_date = row[0]
                        price_date = price_date.replace('.', '-')
                        price_date = price_date.replace('X', '')
                        price_date = price_date.replace('-', '')
                        price_date = '%.8s' % price_date
                        price_close = row[4]
                        if price_close != "open" and price_close != "NA" and i > 1:
                            if i == 2:
                                sep = ''
                            else:
                                sep = ','
                            inserted_values = inserted_values + sep +\
                            "('"+symbol+"',"+price_date+","+price_close+")"
                            debug(symbol +": ("+str(i)+"/"+str(j)+"): "+price_date+": "+\
                                  os.path.basename(__file__) +" - " + inserted_values)
                        i += 1
                    cr_q_ins = connection.cursor(pymysql.cursors.SSCursor)
                    sql_q_ins = "INSERT IGNORE INTO price_instruments_data "+\
                    "(symbol, date, price_close) VALUES " + inserted_values
                    cr_q_ins.execute(sql_q_ins)
                    connection.commit()
                    gc.collect()
                    cr_q_ins.close()
            k += 1
        else:
            break
    cursor.close()
    connection.close()
    log_this('1. quantmod_insert_db_price_data_dsc', 1)

insert_db_price_data_dsc()
