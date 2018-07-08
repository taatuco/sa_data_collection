###############################################################################
# Desc: Transform and compute data for technical analysis
#
# This script prepare and collect technical analysis data to insert in the table
# price_instruments_data. Various scripts are called to calculate and transform data
# to import in the database.
#
# Dependencies: PyMySQL is required to access MySQL database.
# sys, os libraries.
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Date: July 5, 2018
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

#import all TA functions
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_data_collection\\ta_data\\"))
from ta_zeroing_fib_trend import *
from ta_calc_ma import *

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

# Get symbol_list to iterate for records to collect and process
try:
    with connection.cursor() as cursor:
        # Read symbol_list
        sql = "SELECT * FROM symbol_list"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            symbol_quantmod = row["r_quantmod"]
            symbol_index = row["symbol"]
            set_zero_fib_trend(symbol_index)
finally:
    connection.close()
