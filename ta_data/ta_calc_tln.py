# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import csv
import sys
import os
sys.path.append(os.path.abspath("C:\\xampp\\htdocs\\_sa\\sa_pwd"))
from sa_access import *
access_obj = sa_db_access()

import pymysql.cursors
db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

from datetime import datetime, timedelta

class trend_pts:

    sd = datetime.datetime(2000, 1, 1, 1, 1)
    ed = datetime.datetime(2000, 1, 1, 1, 1)
    md = datetime.datetime(2000, 1, 1, 1, 1)

    def __init__(self, p):
        #get end date from query
        pass

    def get_sd(self):
        #get start date: ed - p
        return self.sd

    def get ed(self):
        return self.ed

    def get_md(self):
        #get md = ed - (p/2)
        #md = ed - timedelta(days=p)
        return self.md


class tln_data:

    s = ""
    d = datetime.datetime(2000, 1, 1, 1, 1)
    p = 0
    x_1 = 0

    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    def __init__(self, symbol_id, date_id, period, x_1):
        self.s = symbol_id
        self.d = date_id
        self.p = period
        self.x_1 = x_1

    def get_t_l(self):
        #if (sd > ed ): x = x_1 + ( (ed - sd) / p )
        # else        : x = X_1 + ( (sd - ed) / p )
        pass
