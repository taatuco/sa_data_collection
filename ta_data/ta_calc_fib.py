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

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

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
class fib_data:
    s = ""
    dpv = 0
    dlv = 0
    minp = 0
    maxp = 0
    sd = datetime.datetime(2000, 1, 1, 1, 1)
    fib000 = 0
    fib236 = 0
    fib382 = 0
    fib618 = 0
    fib764 = 0
    fib100 = 0

    def __init__(self, symbol, period):
        try:
            self.s = symbol
            td = datetime.datetime.today().strftime("%Y-%m-%d")
            self.sd = td - ( timedelta(days=period) )
            str_date = self.sd.strftime("%Y%m%d")
            sql_select = "SELECT price_close FROM price_instruments_data "
            sql_max = "SELECT MIN(price_close) FROM price_instruments_data "
            sql_min = "SELECT MAX(price_close) FROM price_instruments_data "

            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = sql_select +\
                    "WHERE symbol='"+ self.s +"' AND date = '"+ str_date +"'"+\
                    " ORDER BY date LIMIT 1"
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                self.dpv = row[0]

            sql = sql_select +\
            "WHERE symbol='" + self.s + " ORDER BY date DESC LIMIT 1"
            cr.execute(cr)
            rs = cr.fetchall()
            for row in rs:
                self.dlv = row[0]

            sql = sql_max +\
            "WHERE symbol='" + self.s + " AND date >='"+str(self.sd) +"'"
            cr.execute(cr)
            rs = cr.fetchall()
            for row in rs:
                self.maxp = row[0]

            sql = sql_min +\
            "WHERE symbol='" + self.s + " AND date >='"+str(self.sd) +"'"
            cr.execute(cr)
            rs = cr.fetchall()
            for row in rs:
                self.minp = row[0]
        finally:
            cr.close()

    def get_fib(self):

        if self.dpv < self.dlv:
            self.fib000 = self.maxp
            self.fib236 = self.fib000 + (self.fib100 - self.fib000) * 0.236
            self.fib382 = self.fib000 + (self.fib100 - self.fib000) * 0.382
            self.fib618 = self.fib000 + (self.fib100 - self.fib000) * 0.618
            self.fib764 = self.fib000 + (self.fib100 - self.fib000) * 0.764
            self.fib100 = self.minp
        else:
            self.fib000 = self.minp
            self.fib236 = self.fib000 - (self.fib100 - self.fib000) * 0.236
            self.fib382 = self.fib000 - (self.fib100 - self.fib000) * 0.382
            self.fib618 = self.fib000 - (self.fib100 - self.fib000) * 0.618
            self.fib764 = self.fib000 - (self.fib100 - self.fib000) * 0.764
            self.fib100 = self.maxp
        f = sett.get_path_ta_data_src +"\\"+ self.s.replace(":","_") +"_fib.csv"
        with open(f, 'w', newline='') as csvfile:
            fieldnames = ["from_date", "fib_0", "fib_236", "fib_382", "fib_618", "fib_764", "fib_100"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({"date": str(self.sd), "fib_0": self.fib000, "fib_236": self.fib236, "fib_382": self.fib382, "fib_618": self.fib618, "fib_764": self.fib764, "fib_100": self.fib100 })
