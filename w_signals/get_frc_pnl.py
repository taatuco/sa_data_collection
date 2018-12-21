# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
from datetime import timedelta
import csv
from pathlib import Path

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

import pymysql.cursors
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def get_forecast_pnl(s,uid):


    td = datetime.datetime.now()
    i = 0
    wdb = 7
    nd = 360


    while i <= nd:

        j = nd - i
        k = (nd - i) + wdb
        pd = datetime.datetime.now() - timedelta(days=k)
        sd = datetime.datetime.now() - timedelta(days=j)
        pd_str = pd.strftime("%Y%m%d")
        sd_str = sd.strftime("%Y%m%d")

        cr = connection.cursor(pymysql.cursors.SSCursor)
        signal = ''
        p_price_close = 0
        p_target_price = 0
        pnl = 0

        print(s +": "+ sd_str +": "+ os.path.basename(__file__) )

        sql = "SELECT price_close, target_price FROM price_instruments_data WHERE symbol ='"+s+"' AND date = "+ pd_str
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            p_price_close = row[0]
            p_target_price = row[1]

        if (p_price_close > 0 and p_target_price > 0 ):

            if p_price_close < p_target_price:
                signal = "b"
            else:
                signal = "s"

            id = 0
            s_pnl = 0
            s_price_close = 0

            sql = "SELECT id, price_close, pnl FROM price_instruments_data WHERE symbol ='"+s+"' AND date = "+ sd_str
            print(sql)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                id = row[0]
                s_price_close = row[1]
                s_pnl = row[2]

            if s_pnl == 0:
                if signal == "b":
                    pnl = s_price_close - p_price_close
                if signal == "s":
                    pnl = p_price_close - s_price_close

                sql = "UPDATE price_instruments_data SET pnl = " + str(pnl) + " WHERE id = " + str(id)
                print(sql)
                try:
                    cr.execute(sql)
                    connection.commit()
                except Exception as e: print(e)

        i += 1