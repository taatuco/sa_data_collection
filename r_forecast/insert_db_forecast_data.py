###############################################################################
# Desc: Read csv and update the database accordingly: table: price_instruments_data
#
# Read csv file and insert records that are not existing in the database table
# price_instruments_data. Existing records are updated according to column price_type.
# This script will import the forecast model results into the price_instruments_data
# table.
#
# Dependencies: PyMySQL is required to access MySQL database.
# datetime library, timedelta library.
# sys, os libraries.
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
sys.path.append(os.path.abspath("../../sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

#define database username and password and other variable regarding access to db
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

# Use csv and file system
import csv
csvdir = "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_forecast\\src\\"
from pathlib import Path

# Date time library
from datetime import datetime, timedelta

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
        sql = "SELECT * FROM symbol_list"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            symbol_quantmod = row["r_quantmod"]
            symbol_index = row["symbol"]
            file_str = csvdir+symbol_quantmod+'.csv'
            filepath = Path(file_str)
            if filepath.exists():
                # Collect the last date from price_instruments_data of the selected symbol
                with connection.cursor() as cursor_last_date:
                    sql_last_date = "SELECT symbol, date FROM price_instruments_data WHERE symbol='"+symbol_index+"' and price_type='p' ORDER by date DESC"
                    cursor_last_date.execute(sql_last_date)
                    result_last_date = cursor_last_date.fetchone()
                    # Collect the last date of the price historical data
                    last_date_is = result_last_date["date"]
                    forecast_date_start = last_date_is + timedelta(days=1)
                # Read csv file
                i = 1
                with open(file_str) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=',')
                    for row in readCSV:
                        # Retrieve csv content
                        # date retrieve the last date and increment.
                        price_date = row[0]
                        price_forecast = row[1]
                        price_low_75 = row[2]
                        price_high_75 = row[3]
                        price_low_85 = row[4]
                        price_high_85 = row[5]
                        price_low_95 = row[6]
                        price_high_95 = row[7]
                        if price_forecast != "Point Forecast":
                            # Check if price_type "f#" already exists. If not create new record, else update.
                            with connection.cursor() as cursor_input_forecast:
                                sql_input_forecast = "SELECT * FROM price_instruments_data WHERE symbol='"+symbol_index+"' and price_type='f"+str(i)+"'"
                                cursor_input_forecast.execute(sql_input_forecast)
                                exists_rec = cursor_input_forecast.fetchone()

                            forecast_date_str = str(forecast_date_start).replace("-","")

                            if not exists_rec:
                                with connection.cursor() as cursor_insert_forecast:
                                    # insert record in case it is not existing
                                    sql_insert_forecast = "INSERT INTO price_instruments_data (symbol, date, price_forecast, price_low_75, price_high_75, price_low_85, price_high_85, price_low_95, price_high_95, price_type) VALUES ('"+symbol_index+"',"+forecast_date_str+","+price_forecast+","+price_low_75+","+price_high_75+","+price_low_85+","+price_high_85+","+price_low_95+","+price_high_95+",'f"+str(i)+"');"
                                    cursor_insert_forecast.execute(sql_insert_forecast)
                                    connection.commit()
                            else:
                                # update the record line
                                with connection.cursor() as cursor_update_forecast:
                                    sql_update_forecast = "UPDATE price_instruments_data SET date = " + forecast_date_str +
                                                            ", price_forecast = " + price_forecast +
                                                            ", price_low_75 = " + price_low_75 +
                                                            ", price_high_75 = " + price_high_75 +
                                                            ", price_low_85 = " + price_low_85 +
                                                            ", price_high_85 = " + price_high_85 +
                                                            ", price_low_95 = " + price_low_95 +
                                                            ", price_high_95 = " + price_high_95 +
                                                            " WHERE symbol ='"+symbol_index+"' AND price_type='f"+str(i)+"'"
                                    cursor_update_forecast.execute(sql_update_forecast)
                                    connection.commit()

                            i += 1
                            forecast_date_start = forecast_date_start + timedelta(days=1)

finally:
    connection.close()
