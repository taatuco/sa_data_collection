# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

'''
(CHANGE) = current_close_price - previous_close_price
(GAIN) = if( (CHANGE)<0, 0, (CHANGE) )
(LOSS) = if( (CHANGE)<0, (CHANGE)* -1, 0 )
(FIRST_AVG, GAIN, LOSS) = AVERAGE( (GAIN) ), AVERAGE( (LOSS) ) (if count> rsi_period)
(AVG_GAIN) = ( (PREVIOUS_AVG_GAIN)*(rsi_period-1)+ (GAIN) ) / rsi_period
(AVG_LOSS) = ( (PREVIOUS_AVG_LOSS)*(rsi_period-1)+ (LOSS) ) / rsi_period
(RS) = (AVG_GAIN) / (AVG_LOSS)
(RSI) = if( (RS)=0, 100, 100-(100/1+(RS)) )
'''

def calc_rsi(symbol_index, date_index, rsi_period):
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
    try:
        rsi_period = str(rsi_period)
        with connection.cursor() as cursor:



    finally:
        connection.close()
