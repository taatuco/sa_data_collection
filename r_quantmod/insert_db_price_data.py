###############################################################################
# Desc: Read csv and update the database accordingly: table: price_instruments_data
#
# Read csv file and insert records that are not existing in the database table
# price_instruments_data. (Avoid duplicate records).
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Date: July 2, 2018
###############################################################################
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

import csv
csvdir = "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_quantmod\\src\\"
from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Get symbol_list to iterate for records to collect
try:
    with connection.cursor() as cr:
        # Read symbol_list
        sql = "SELECT symbol, r_quantmod FROM symbol_list"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            symbol_quantmod = row["r_quantmod"]
            s = row["symbol"]
            file_str = csvdir+symbol_quantmod+'.csv'
            filepath = Path(file_str)
            if filepath.exists():
                # Read csv file
                with open(file_str) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=',')
                    for row in readCSV:
                        # For each symbol, retrieve the csv content
                        price_date = row[0]

                        price_date = price_date.replace('.', '-')
                        price_date = price_date.replace('X', '')
                        price_date = price_date.replace('-','')
                        price_date = '%.8s' % price_date
                        price_open = row[1]
                        price_high = row[2]
                        price_low = row[3]
                        price_close = row[4]
                        volume = row[5]
                        # check for each row if not already exists.
                        # if exists, then insert new record, else ignore.
                        if price_open != "open" and price_open != "NA":
                            with connection.cursor() as cr_q_cnt:
                                sql_q_cnt = "SELECT id FROM price_instruments_data WHERE symbol='"+s+"' AND date='"+price_date+"'"
                                cr_q_cnt.execute(sql_q_cnt)
                                exists_rec = cr_q_cnt.fetchall()
                                print(sql_q_cnt)

                                if not exists_rec:
                                    # insert record in case not existing.
                                    with connection.cursor() as cr_q_ins:
                                        sql_q_ins = "INSERT INTO price_instruments_data (symbol, date, price_close, price_open, price_low, price_high, volume) VALUES ('"+s+"',"+price_date+","+price_close+","+price_open+","+price_low+","+price_high+","+volume+");"
                                        cr_q_ins.execute(sql_q_ins)
                                        connection.commit()
                                        cr_q_ins.close()
                                cr_q_cnt.close()
finally:
    connection.close()
