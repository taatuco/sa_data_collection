""" Functionalities related to trend lines """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import datetime
from datetime import timedelta
import csv
import sys
import os
import os.path
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

class TrendPoints:
    """
    Retrieve data points related to trend lines
    Args:
        String: Instrument symbol
        Integer: Period
    """
    import pymysql.cursors
    sday = datetime.datetime(2000, 1, 1, 1, 1)
    eday = datetime.datetime(2000, 1, 1, 1, 1)
    mday = datetime.datetime(2000, 1, 1, 1, 1)
    symbol = ""
    period = 0
    period2 = 0

    def __init__(self, symbol, period):
        """ Initialize data points related to trend lines """
        self.symbol = symbol
        self.period = period
        self.period2 = period/2
        connection = TrendPoints.pymysql.connect(host=DB_SRV,
                                                 user=DB_USR,
                                                 password=DB_PWD,
                                                 db=DB_NAME,
                                                 charset='utf8mb4',
                                                 cursorclass=TrendPoints.pymysql.cursors.DictCursor)
        cursor = connection.cursor(TrendPoints.pymysql.cursors.SSCursor)
        sql = "SELECT date FROM price_instruments_data "+\
                "WHERE symbol='"+ self.symbol +\
                "' ORDER BY date DESC LIMIT 1"
        cursor.execute(sql)
        res = cursor.fetchall()

        for row in res:
            self.eday = row[0]
        cursor.close()
        connection.close()
        self.sday = self.eday - timedelta(days=self.period)
        self.mday = self.eday - timedelta(days=self.period2)

    def get_sd(self):
        """ Get start date of the trend line """
        return self.sday

    def get_ed(self):
        """ Get end date of the trend line """
        return self.eday

    def get_md(self):
        """ Get the middle point of the trend line"""
        return self.mday

    def get_val_frm_d(self, date_this, get_what):
        """ Get the trend line points from date """
        value = 0
        connection = TrendPoints.pymysql.connect(host=DB_SRV,
                                                 user=DB_USR,
                                                 password=DB_PWD,
                                                 db=DB_NAME,
                                                 charset='utf8mb4',
                                                 cursorclass=TrendPoints.pymysql.cursors.DictCursor)
        cursor = connection.cursor(TrendPoints.pymysql.cursors.SSCursor)
        date_range = ""
        selection = ""
        if date_this == self.sday:
            date_range = "' AND date>'"+str(self.sday)+"' AND date<'"+str(self.mday)+"'"
        if date_this == self.eday:
            date_range = "' AND date>'"+str(self.mday)+"' AND date<'"+str(self.eday)+"'"
        if get_what == "l":
            selection = "SELECT MIN(price_close) AS p "
        if get_what == "h":
            selection = "SELECT MAX(price_close) AS p "

        sql = selection + "FROM price_instruments_data WHERE symbol='"+self.symbol + date_range
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            value = row[0]
        cursor.close()
        connection.close()
        if value is None:
            value = 0
        return value

class TrendData:
    """
    Data related to trend lines
    Args:
        String: Instrument symbol
        Integer: Period
        String: lower or higher trend line.
    """
    import pymysql.cursors
    sdate = datetime.datetime(2000, 1, 1, 1, 1)
    edate = datetime.datetime(2000, 1, 1, 1, 1)
    mdate = datetime.datetime(2000, 1, 1, 1, 1)
    get_this = ""
    sdv = 0
    edv = 0
    period = 0
    symbol = ""

    def __init__(self, symbol, period, get_what):
        """ Initialize trend line """
        pts = TrendPoints(symbol, period)
        self.symbol = symbol
        self.sdate = pts.get_sd()
        self.edate = pts.get_ed()
        self.mdate = pts.get_md()
        self.period = period
        self.get_this = get_what
        self.sdv = pts.get_val_frm_d(self.sdate, self.get_this)
        self.edv = pts.get_val_frm_d(self.edate, self.get_this)

    def get_slope(self):
        """ Get trend line slope """
        slp = 0
        if self.period != 0:
            slp = (self.edv - self.sdv)/self.period
        return slp

    def get_sd(self):
        """ Get trend line start date """
        return self.sdate

    def get_ed(self):
        """ Get trend line end date """
        return self.edate

    def get_sdv(self):
        """ Get start date value """
        return self.sdv

    def get_edv(self):
        """ Get end date value """
        return self.edv

    def get_200ma_frm_d(self, date_this):
        """ Get 200 moving average from date """
        val = 0
        connection = TrendData.pymysql.connect(host=DB_SRV,
                                               user=DB_USR,
                                               password=DB_PWD,
                                               db=DB_NAME,
                                               charset='utf8mb4',
                                               cursorclass=TrendData.pymysql.cursors.DictCursor)
        cursor = connection.cursor(TrendData.pymysql.cursors.SSCursor)
        sql = "SELECT ma200 FROM price_instruments_data WHERE (symbol ='"+self.symbol+\
        "' AND date='"+str(date_this)+"') LIMIT 1"
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            val = row[0]
        cursor.close()
        return val

    def get_50ma_frm_d(self, date_this):
        """ Get 50 moving average from date """
        val = 0
        connection = TrendData.pymysql.connect(host=DB_SRV,
                                               user=DB_USR,
                                               password=DB_PWD,
                                               db=DB_NAME,
                                               charset='utf8mb4',
                                               cursorclass=TrendData.pymysql.cursors.DictCursor)
        cursor = connection.cursor(TrendData.pymysql.cursors.SSCursor)
        sql = "SELECT AVG(price_close) AS p FROM price_instruments_data WHERE (symbol ='"+\
        self.symbol+"' AND date<='"+str(date_this)+"') LIMIT 50"
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            val = row[0]
        cursor.close()
        return val

    def get_rsi_avg(self, date_this, period):
        """ Retrieve relative strength index from date, period """
        val = 0
        connection = TrendData.pymysql.connect(host=DB_SRV,
                                               user=DB_USR,
                                               password=DB_PWD,
                                               db=DB_NAME,
                                               charset='utf8mb4',
                                               cursorclass=TrendData.pymysql.cursors.DictCursor)
        cursor = connection.cursor(TrendPoints.pymysql.cursors.SSCursor)
        sql = "SELECT AVG(rsi14) AS rsi FROM price_instruments_data WHERE (symbol ='"+\
        self.symbol+"' AND date<='"+str(date_this)+"') LIMIT " + str(period)
        cursor.execute(sql)
        res = cursor.fetchall()
        for row in res:
            val = row[0]
        cursor.close()
        return val

    def get_rsi_mom(self, val):
        """ Retrieve relative strength index momentum value """
        mom = ""
        if val < 31:
            mom = "Oversold"
        if val > 30 and val < 50:
            mom = "Weak"
        if val > 49 and val < 70:
            mom = "Strong"
        if val > 69:
            mom = "Overbought"
        return mom

def get_bias(sdv, edv):
    """
    Get trend line bias
    Args:
        Double: Start date value
        Double: End date value
    Returns:
        String: Bias
    """
    ret = "Neutral"
    if sdv > edv:
        ret = "Negative"
    if sdv < edv:
        ret = "Positive"
    return ret

def get_trend_line_data(symbol, uid):
    """
    Compute trend lines data
    Args:
        String: Instrument symbol
        Integer: Instrument uid
    Returns:
        None
    """
    tl_180_l = TrendData(symbol, 180, "l")
    tl_180_h = TrendData(symbol, 180, "h")
    tl_360_l = TrendData(symbol, 360, "l")
    tl_360_h = TrendData(symbol, 360, "h")
    file_this = SETT.get_path_src()+"\\"+str(uid)+"t.csv"
    with open(file_this, 'w', newline='') as csvfile:
        fieldnames = ["180_sd", "180_slope_low", "180_slope_high",
                      "360_sd", "360_slope_low", "360_slope_high",
                      "180_sdv_low", "180_sdv_high", "360_sdv_low", "360_sdv_high",
                      "st_lower_range", "st_upper_range", "lt_lower_range", "lt_upper_range",
                      "st_rsi_avg", "lt_rsi_avg", "st_rsi_mom", "lt_rsi_mom",
                      "ma200", "ma50", "st_bias", "lt_bias"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        t180_sd = tl_180_l.get_sd()
        t180_ed = tl_180_l.get_ed()
        t360_ed = tl_360_l.get_ed()
        t180_slp_l = tl_180_l.get_slope()
        t180_slp_h = tl_180_h.get_slope()
        t360_sd = tl_360_l.get_sd()
        t360_slp_l = tl_360_l.get_slope()
        t360_slp_h = tl_360_h.get_slope()
        t180_sdv_l = tl_180_l.get_sdv()
        t180_sdv_h = tl_180_h.get_sdv()
        t360_sdv_l = tl_360_l.get_sdv()
        t360_sdv_h = tl_360_h.get_sdv()
        st_lower_range = tl_180_l.get_edv()
        st_upper_range = tl_180_h.get_edv()
        lt_lower_range = tl_360_l.get_edv()
        lt_upper_range = tl_360_h.get_edv()

        st_rsi_avg = tl_180_l.get_rsi_avg(t180_ed, 5)
        lt_rsi_avg = tl_360_l.get_rsi_avg(t360_ed, 50)

        st_rsi_mom = tl_180_l.get_rsi_mom(st_rsi_avg)
        lt_rsi_mom = tl_360_l.get_rsi_mom(lt_rsi_avg)
        ma_200_ed = tl_360_l.get_200ma_frm_d(t180_ed)
        ma_50_ed = tl_360_l.get_50ma_frm_d(t180_ed)
        ma_200_sd = tl_360_l.get_200ma_frm_d(t180_sd)
        ma_50_sd = tl_360_l.get_50ma_frm_d(t180_sd)
        st_bias = get_bias(ma_50_sd, ma_50_ed)
        lt_bias = get_bias(ma_200_sd, ma_200_ed)

        debug(symbol +": "+ os.path.basename(__file__))
        writer.writerow({"180_sd": str(t180_sd),
                         "180_slope_low": str(t180_slp_l),
                         "180_slope_high": str(t180_slp_h),
                         "360_sd": str(t360_sd),
                         "360_slope_low": str(t360_slp_l),
                         "360_slope_high": str(t360_slp_h),
                         "180_sdv_low": str(t180_sdv_l),
                         "180_sdv_high": str(t180_sdv_h),
                         "360_sdv_low": str(t360_sdv_l),
                         "360_sdv_high": str(t360_sdv_h),
                         "st_lower_range": str(st_lower_range),
                         "st_upper_range": str(st_upper_range),
                         "lt_lower_range": str(lt_lower_range),
                         "lt_upper_range": str(lt_upper_range),
                         "st_rsi_avg":str(st_rsi_avg),
                         "lt_rsi_avg": str(lt_rsi_avg),
                         "st_rsi_mom": str(st_rsi_mom),
                         "lt_rsi_mom": str(lt_rsi_mom),
                         "ma200": str(ma_200_ed),
                         "ma50": str(ma_50_ed),
                         "st_bias": str(st_bias),
                         "lt_bias": str(lt_bias)})
    