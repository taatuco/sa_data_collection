""" Functionalities related to price variation """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import csv
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_count_d(symbol, count_what, period):
    """
    Count number of days in the upside or downside as per args.
    Args:
        String: Instrument symbol
        Integer: 1 or -1: if 1 then count upside else downside
        Integer: number of period
    Returns:
        Integer: count of number of occurence as per args.
    """
    cnt = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql_select = "SELECT COUNT(id) FROM price_instruments_data WHERE symbol = '"+ symbol +"' "

    if count_what == 1:
        sql_t_cond = "AND change_1d>=0 "
    else:
        sql_t_cond = "AND change_1d<0 "

    sql_p_cond = " AND date>= DATE(DATE_ADD(curdate(), INTERVAL -"+ str(period) +" DAY))"

    sql = sql_select + sql_t_cond + sql_p_cond
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        cnt = row[0]
    cursor.close()
    connection.close()
    return cnt

def get_day_up_dwn_stat(symbol, uid):
    """
    Write to csv file count results
    Args:
        String: Instrument symbol
        Integer: Instrument unique ID
    Returns:
        None
    """
    m1_up = get_count_d(symbol, 1, 30)
    m1_dn = get_count_d(symbol, -1, 30)
    w1_up = get_count_d(symbol, 1, 7)
    w1_dn = get_count_d(symbol, -1, 7)

    file_this = SETT.get_path_src()+"\\"+str(uid)+"ud.csv"
    with open(file_this, 'w', newline='') as csvfile:
        fieldnames = ["symbol", "7_up_days", "7_down_days", "30_up_days", "30_down_days"]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        debug(symbol +": "+ os.path.basename(__file__))
        writer.writerow({"symbol": str(symbol),
                         "7_up_days": str(w1_up), "7_down_days": str(w1_dn),
                         "30_up_days": str(m1_up), "30_down_days": str(m1_dn)})
