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
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Date: July 2, 2018
# Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
###############################################################################

#define database username and password and other variable regarding access to db
db_usr = 'sa_db_user'
db_pwd = '9XHWVxTH9ZJnshvN'
db_name = 'smartalpha'
db_srv = 'localhost'

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
                        #date retrieve the last date and increment.
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
                            print(i)
                            print(price_forecast)
                            i += 1

finally:
    connection.close()
