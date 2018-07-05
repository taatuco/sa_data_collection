# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

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
            symbol_index = row["symbol"]
            # Select only rows from price_instruments_data with ma200
            with connection.cursor() as cursor_price_data:
                sql_price_data = "SELECT symbol, date, ma200 FROM price_instruments_data "+\
                      "WHERE symbol='"+symbol_index+"' AND ma200=0 ORDER BY date DESC"
                cursor_price_data.execute(sql_price_data)
                result_price_data = cursor_price_data.fetchall()
                for row in result_price_data:
                    date_index = str(row["date"]).replace("-","")
                    # For each date get the average price for 200 period
                    with connection.cursor() as cursor_price_avg:
                        sql_price_avg = "SELECT AVG(price_close) AS avg200 "+\
                                        "FROM (SELECT symbol, date, ma200, price_close "+\
                                        "FROM price_instruments_data WHERE symbol='"+symbol_index+"' AND "+\
                                        "date<"+date_index+" LIMIT 200) avg_table"
                        cursor_price_avg.execute(sql_price_avg)
                        result_price_avg = cursor_price_avg.fetchall()
                        for row in result_price_avg:
                            ma200 = str(row["avg200"])
                        # Update ma200 column
                        with connection.cursor() as cursor_ma200_update:
                            sql_ma200_update = "UPDATE FROM price_instruments_data "+\
                                               "SET ma200 ="+ma200 +\
                                               " WHERE symbol='"+symbol_index+"' AND date="+ date_index
                            print(sql_ma200_update)
                            cursor_ma200_update.execute(sql_ma200_update)
                            connection.commit()

finally:
    connection.close()
