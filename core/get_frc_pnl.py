""" Collect forecast profit and loss """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
from datetime import timedelta
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


def get_forecast_pnl(symbol, number_of_day_collection, full_update, connection):
    """
    Get forecast profit and loss
    Args:
        String: Symbol of the instrument
        Integer: Number of day back in history to collect
        Boolean: If full_update is set to True, compute every record with range.
    Returns:
        None
    """
    i = 0
    wdb = 7
    while i <= number_of_day_collection:
        j = number_of_day_collection - i
        k = (number_of_day_collection - i) + wdb
        previous_date = datetime.datetime.now() - timedelta(days=k)
        selected_date = datetime.datetime.now() - timedelta(days=j)
        pd_str = previous_date.strftime("%Y%m%d")
        sd_str = selected_date.strftime("%Y%m%d")

        signal = ''
        p_price_close = 0
        p_target_price = 0
        pnl = 0
        pnl_long = 999
        pnl_short = 999

        debug(symbol +": "+ sd_str +": "+ os.path.basename(__file__))

        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT price_close, target_price FROM price_instruments_data "+\
        "WHERE symbol ='"+symbol+"' AND date = "+ pd_str
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            p_price_close = row[0]
            p_target_price = row[1]
        cursor.close()

        if (p_price_close > 0 and p_target_price > 0):

            if p_price_close < p_target_price:
                signal = "b"
            else:
                signal = "s"

            pid_id = 0
            s_pnl = 0
            s_pnl_long = 0
            s_pnl_short = 0
            s_price_close = 0

            cursor = connection.cursor(pymysql.cursors.SSCursor)
            sql = "SELECT id, price_close, pnl, pnl_long, pnl_short "+\
            "FROM price_instruments_data WHERE symbol ='"+symbol+"' AND date = "+ sd_str
            debug(sql)
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                pid_id = row[0]
                s_price_close = row[1]
                s_pnl = row[2]
                s_pnl_long = row[3]
                s_pnl_short = row[4]
            cursor.close()

            if (s_pnl == 0 or s_pnl_long == 0 or s_pnl_short == 0) or (full_update):
                if signal == "b":
                    pnl = s_price_close - p_price_close
                    pnl_long = pnl
                if signal == "s":
                    pnl = p_price_close - s_price_close
                    pnl_short = pnl

                cursor = connection.cursor(pymysql.cursors.SSCursor)
                sql = "UPDATE price_instruments_data SET pnl = " + str(pnl) +\
                ", pnl_long = " + str(pnl_long) + ", pnl_short = " + str(pnl_short) +\
                " WHERE id = " + str(pid_id)
                debug(sql)
                cursor.execute(sql)
                connection.commit()
                cursor.close()
        i += 1
