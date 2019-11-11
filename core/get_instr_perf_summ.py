""" Get information related to instrument such as performance """
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
from settings import SmartAlphaPath, debug, get_portf_suffix
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_pct_from_date(date_from, sql_select, last_price):
    """
    Get percentage performance from specified date to current date.
    Args:
        String: date in string format YYYYMMDD
        String: SQL query to select the appropriate column
        Double: Last price
    Returns:
        Double: Percentage performance
    """
    pct = 0
    initial_price = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = sql_select + "AND date <= '"+ str(date_from) +"' ORDER BY date DESC LIMIT 1"
    debug(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        initial_price = row[0]
    cursor.close()
    connection.close()
    debug('pp: ' + str(initial_price) + ' date='+ str(date_from))
    if initial_price != 0:
        pct = ((last_price - initial_price) / initial_price)
    debug(str(pct) + ' = '+ '('+ str(last_price) +' - '+\
              str(initial_price) +') / '+ str(initial_price))
    return pct

def get_prev_session_date(symbol):
    """
    Get the last date of the last trading session
    Args:
        String: Instrument symbol
    Returns:
        Datetime: last trading session date
    """
    ret = datetime.datetime(2000, 1, 1, 1, 1)
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT date from price_instruments_data WHERE symbol = '"+\
    str(symbol) +"' ORDER BY date DESC LIMIT 2"
    cursor.execute(sql)
    res = cursor.fetchall()
    i = 1
    for row in res:
        if i == 2:
            ret = row[0]
        i += 1
    cursor.close()
    connection.close()
    return ret


class InstrumentSummaryData:
    """
    Provide information related to trading instrument
    Args:
        String: Instrument symbol
        Int: id of the symbol
    """
    symbol_selection = ""
    uid = ""
    sql_select = ""
    sql_select_signal = ""
    last_date = datetime.datetime(2000, 1, 1, 1, 1)
    d_1yp = datetime.datetime(2000, 1, 1, 1, 1)
    d_6Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_3Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Mp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Dp = datetime.datetime(2000, 1, 1, 1, 1)
    d_1Wf = datetime.datetime(2000, 1, 1, 1, 1)
    last_price = 0
    lp_signal = 0

    def __init__(self, symbol, uid):
        """ Select and initialize instrument data according to args """
        self.symbol_selection = symbol
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol from symbol_list WHERE uid=" + str(uid)
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            symbol_is_portf = row[0]
        if symbol_is_portf.find(get_portf_suffix()) > -1:
            self.sql_select = "SELECT price_close, date FROM chart_data "+\
            "WHERE symbol='"+ self.symbol_selection +"' "
        else:
            self.sql_select = "SELECT price_close, date "+\
            "FROM price_instruments_data WHERE symbol='"+ self.symbol_selection + "' "
            self.sql_select_signal = "SELECT signal_price, date FROM chart_data "+\
            "WHERE symbol='"+ self.symbol_selection +"' AND forecast = 0 "
            sql = self.sql_select_signal+" ORDER BY Date DESC LIMIT 1"
            debug(sql)
            cursor.execute(sql)
            res = cursor.fetchall()
            for row in res:
                self.lp_signal = row[0]

        sql = self.sql_select+" ORDER BY Date DESC LIMIT 1"
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            self.last_price = row[0]
        self.last_date = row[1]
        cursor.close()
        connection.close()

        self.uid = uid
        self.d_1_year_perf = self.last_date - (timedelta(days=365))
        self.d_6_month_perf = self.last_date - (timedelta(days=180))
        self.d_3_month_perf = self.last_date - (timedelta(days=90))
        self.d_1_month_perf = self.last_date - (timedelta(days=30))
        self.d_1_week_perf = self.last_date - (timedelta(days=7))
        self.d_1_day_perf = get_prev_session_date(self.symbol_selection)
        self.d_1_week_forcast = 0

    def get_last_price(self):
        """ get last trading session price """
        return self.last_price

    def get_ticker(self):
        """ get instrument symbol """
        return self.symbol_selection

    def get_pct_1_year_performance(self):
        """ get instrument 1-year performance """
        str_date = self.d_1_year_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.last_price))

    def get_pct_6_month_performance(self):
        """ get instrument 6-month performance """
        str_date = self.d_6_month_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.last_price))

    def get_pct_3_month_performance(self):
        """ get instrument 3-month performance """
        str_date = self.d_3_month_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.last_price))

    def get_pct_1_month_performance(self):
        """ get instrument 1-month performance """
        str_date = self.d_1_month_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.last_price))

    def get_pct_1_week_performance(self):
        """ get instrument 1-week performance """
        str_date = self.d_1_week_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.last_price))

    def get_pct_1_day_performance(self):
        """ get instrument 1-day performance """
        str_date = self.d_1_day_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select, self.last_price))

    def get_pct_1_year_signal(self):
        """ get instrument 1-year signal performance """
        str_date = self.d_1_year_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_6_month_signal(self):
        """ get instrument 6-month signal performance """
        str_date = self.d_6_month_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_3_month_signal(self):
        """ get instrument 3-month signal performance """
        str_date = self.d_3_month_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1_month_signal(self):
        """ get instrument 1-month signal performance """
        str_date = self.d_1_month_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))

    def get_pct_1_week_signal(self):
        """ get instrument 1-week signal performance """
        str_date = self.d_1_week_perf.strftime("%Y%m%d")
        return str(get_pct_from_date(str_date, self.sql_select_signal, self.lp_signal))
