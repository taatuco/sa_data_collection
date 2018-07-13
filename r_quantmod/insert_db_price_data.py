###############################################################################
# Desc: Read csv and update the database accordingly: table: price_instruments_data
#
# Read csv file and insert records that are not existing in the database table
# price_instruments_data. (Avoid duplicate records).
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Date: July 2, 2018
###############################################################################

# Licensed under The MIT License
# Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#import db access object
import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

#define database username and password and other variable regarding access to db
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

# Use csv and file system
import csv
csvdir = "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_quantmod\\src\\"
from pathlib import Path

# Use PyMySQL to access MySQL database
import pymysql.cursors

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Get symbol_list to iterate for records to collect
try:
    with connection.cursor() as cursor:
        # Read symbol_list
        sql = "SELECT symbol, r_quantmod FROM symbol_list"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            symbol_quantmod = row["r_quantmod"]
            symbol_index = row["symbol"]
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
                            with connection.cursor() as query_count_cursor:
                                query_count_sql = "SELECT id FROM price_instruments_data WHERE symbol='"+symbol_index+"' AND date='"+price_date+"'"
                                query_count_cursor.execute(query_count_sql)
                                exists_rec = query_count_cursor.fetchall()
                                print(query_count_sql)

                                if not exists_rec:
                                    # insert record in case not existing.
                                    with connection.cursor() as query_insert_cursor:
                                        insert_price_sql = "INSERT INTO price_instruments_data (symbol, date, price_close, price_open, price_low, price_high, volume) VALUES ('"+symbol_index+"',"+price_date+","+price_close+","+price_open+","+price_low+","+price_high+","+volume+");"
                                        query_insert_cursor.execute(insert_price_sql)
                                        connection.commit()
                                        query_insert_cursor.close()

                                query_count_cursor.close()
finally:
    connection.close()
