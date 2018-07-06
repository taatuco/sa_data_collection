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

def drop_tmp_v_view():
    # Drop the view
    try:
        with connection.cursor() as cursor_drop_view:
            sql_drop_view = "DROP VIEW tmp_v_ma200"
            cursor_drop_view.execute(sql_drop_view)
            connection.commit()
    except:
        pass

def calc_ma():
    try:
        # Get list of symbols
        with connection.cursor() as cursor_list_symbol:
            sql_list_symbol = "SELECT * FROM symbol_list"
            cursor_list_symbol.execute(sql_list_symbol)
            result_list_symbol = cursor_list_symbol.fetchall()
            for row in result_list_symbol:
                symbol_index = row["symbol"]
                # Get each date
                with connection.cursor() as cursor_list_price:
                    sql_list_price = "SELECT symbol, date, price_close, ma200 "+\
                                     "FROM price_instruments_data "+\
                                     "WHERE symbol = '"+symbol_index+"' AND ma200 = 0 AND price_type='p' ORDER BY symbol, date DESC"
                    cursor_list_price.execute(sql_list_price)
                    result_list_price = cursor_list_price.fetchall()
                    for row in result_list_price:
                        date_index = str(row["date"]).replace("-","")
                        drop_tmp_v_view()
                        # Create temporary SQL view to get ma200 value

                        with connection.cursor() as cursor_create_view:
                            sql_create_view = "CREATE VIEW tmp_v_ma200 AS "+\
                                  "(SELECT symbol, avg(price_close) as 'ma200' "+\
                                  "FROM price_instruments_data "+\
                                  "WHERE Symbol = '"+symbol_index+"' AND Date<"+date_index+" "+\
                                  "LIMIT 200)"
                            cursor_create_view.execute(sql_create_view)
                            connection.commit()
                        # Collect value from the view
                        with connection.cursor() as cursor_get_value:
                            sql_get_value = "SELECT * FROM tmp_v_ma200"
                            cursor_get_value.execute(sql_get_value)
                            result_get_value = cursor_get_value.fetchall()
                            for row in result_get_value:
                                ma200_str = str(row["ma200"])
                        try:
                            # Update value in price_instruments_data
                            with connection.cursor() as cursor_update:
                                sql_update = "UPDATE price_instruments_data "+\
                                             "SET ma200 = "+ ma200_str +" WHERE symbol ='"+symbol_index+"' AND date = "+date_index
                                cursor_update.execute(sql_update)
                                connection.commit()
                        except:
                            pass

                        # Remove view
                        drop_tmp_v_view()

    finally:
        connection.close()
