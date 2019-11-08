# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime; import time; from datetime import timedelta
from sa_numeric import *

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

sys.path.append(os.path.abspath( sett.get_path_core() ))
from ta_calc_ma import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()


def get_trades(s,uid,dc,full_update):

    r = False
    try:
        daycount = dc + 10
        dfrom = datetime.datetime.now() - timedelta(days=daycount) ; dfrom_str = dfrom.strftime('%Y%m%d')

        trade_symbol = s; trade_order_type = ''
        trade_entry_price = ''; trade_entry_date = dfrom
        trade_expiration_date = dfrom; trade_close_price = -1
        trade_pnl_pct = 0; trade_status = ''; trade_last_price = 0
        trade_decimal_places = 0; trade_url = "s/?uid="+ str(uid)

        if full_update:
            sql_delete_trades = "DELETE FROM trades WHERE symbol = '"+ s +"' "
        else:
            sql_delete_trades = "DELETE FROM trades WHERE symbol ='"+ s +"' AND status='active' "

        import pymysql.cursors
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = sql_delete_trades
        cr.execute(sql)
        connection.commit()
        cr.close()

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT decimal_places, fullname FROM instruments WHERE symbol = '"+ s +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            trade_decimal_places = row[0]
            trade_fullname = row[1].replace("'","`")
        cr.close()

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT price_close FROM price_instruments_data WHERE symbol = '"+ s +"' ORDER BY date DESC LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: trade_last_price = row[0]
        cr.close()

        cr_1 = connection.cursor(pymysql.cursors.SSCursor)
        sql_1 = "SELECT symbol, date, price_close, target_price "+\
        "FROM price_instruments_data WHERE symbol = '"+ s +"' AND date >=" + dfrom_str + " ORDER BY date"
        cr_1.execute(sql_1)
        rs_1 = cr_1.fetchall()
        i = 0
        inserted_value = ''
        for row in rs_1:
            symbol_1 = row[0]
            date_1 = row[1]
            price_close_1 = round( row[2], trade_decimal_places)
            target_price_1 = round( row[3], trade_decimal_places)

            dto = date_1 + timedelta(days=8) ; dto_str = dto.strftime('%Y%m%d')
            cr_2 = connection.cursor(pymysql.cursors.SSCursor)
            sql_2 = "SELECT date, price_close FROM price_instruments_data WHERE symbol = '"+ s +"' AND date >=" + dto_str + " ORDER BY date LIMIT 1"
            debug(sql_2)
            cr_2.execute(sql_2)
            rs_2 = cr_2.fetchall()
            date_2 = None; price_close_2 = -1
            for row in rs_2: date_2 = row[0]; price_close_2 = round( row[1], trade_decimal_places)
            cr_2.close()

            if target_price_1 != -9:
                if price_close_1 <= target_price_1: trade_order_type = 'buy'
                if price_close_1 > target_price_1: trade_order_type = 'sell'

            debug(str(date_1) + " ::: " + str(price_close_1) + " ::: " + str(target_price_1) + " ::: " + str(trade_order_type) )

            trade_entry_price = price_close_1; trade_entry_date = date_1 + timedelta(days=1)
            if date_2 is not None: trade_expiration_date = date_2
            else: trade_expiration_date = date_1 + timedelta(days=8)
            trade_close_price = price_close_2
            if price_close_2 == -1:
                trade_status = 'active'
                if trade_order_type == 'buy': trade_pnl_pct = get_pct_change(price_close_1, trade_last_price)
                else: trade_pnl_pct = get_pct_change(trade_last_price, price_close_1)

            else:
                trade_status = 'expired'
                if trade_order_type == 'buy': trade_pnl_pct = get_pct_change(price_close_1, price_close_2)
                else: trade_pnl_pct = get_pct_change(price_close_2, price_close_1)

            if i == 0:
                sep = ''
            else:
                sep = ','

            if target_price_1 != -9:
                debug("("+  str(uid)  +", '"+ trade_symbol +"', '"+ trade_fullname  +"', '" + trade_order_type +"',"+ str(trade_entry_price) +",'"+ str(trade_entry_date) +"','"+\
                str(trade_expiration_date) +"',"+ str(trade_close_price) +","+ str(trade_pnl_pct) +",'"+ str(trade_status) +"', '"+ str(trade_url) + "' " +")")

                inserted_value = inserted_value + sep + "("+  str(uid)  +", '"+ trade_symbol +"', '"+ trade_fullname  +"', '" + trade_order_type +"',"+ str(trade_entry_price) +",'"+ str(trade_entry_date) +"','"+\
                str(trade_expiration_date) +"',"+ str(trade_close_price) +","+ str(trade_pnl_pct) +",'"+ str(trade_status) +"', '"+ str(trade_url) + "' " +")"
                i += 1

        cr_1.close()

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "INSERT IGNORE INTO trades(uid, symbol, fullname, order_type, entry_price, entry_date, expiration_date, close_price, pnl_pct, status, url) VALUES "+ inserted_value
        try:
            debug(sql_i)
            cr_i.execute(sql_i)
            connection.commit()
            r = True
        except:
            pass
        cr_i.close()
        connection.close()

    except Exception as e: debug(e)

    return r
