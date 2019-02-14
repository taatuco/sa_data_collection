# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os


sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


class sa_path:
    rdir = os.path.dirname(os.path.realpath(__file__))
    pdir = os.path.abspath(os.path.join(rdir, os.pardir))

    def get_path_pwd(self):
        return self.pdir+ "\\sa_pwd"

    def get_path_src(self):
        return self.rdir+"\\src\\"

    def get_path_labels(self):
        return self.rdir + "\\labels"

    def get_path_feed(self):
        return self.rdir + "\\feed"

    def get_path_core(self):
        return self.rdir + "\\core"

    def get_path_portfolios(self):
        return self.rdir + "\\portfolios"

    def get_path_r_quantmod_src(self):
        return self.rdir + "\\r_quantmod\\src\\"

    def get_path_r_oanda_src(self):
        return self.rdir + "\\r_oanda\\src\\"

def get_portf_suffix():
    return "PRF:"

def get_product_name():
    return "SmartAlpha"

def get_user_smartalpha_id():
    sa_bot_nickname = 'smartalpha'
    r = ''
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT id FROM users WHERE nickname = '"+ sa_bot_nickname +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: print(e)
    return r
