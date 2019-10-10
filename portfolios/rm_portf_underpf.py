# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import gc
import datetime
import time

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors

def rm_portf_underpf(limit_max):
    total = 0
    quant_to_rm = 0
    try:
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT COUNT(*) FROM instruments JOIN users ON instruments.owner = users.id'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: total = row[0]
        cr.close()

        quant_to_rm = int(total) - int(limit_max)


        if quant_to_rm > 0:
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = 'SELECT instruments.symbol, users.is_bot '+\
            'FROM instruments JOIN users ON instruments.owner = users.id '+\
            'WHERE users.is_bot=1 AND instruments.symbol LIKE "%'+ get_portf_suffix() +'%" ORDER BY instruments.y1 '+\
            'LIMIT '+ str(quant_to_rm)
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs:
                s = row[0]
                rm_portf_from('feed','symbol',s)
                rm_portf_from('chart_data','symbol',s)
                rm_portf_from('portfolios','portf_symbol',s)
                rm_portf_from('instruments','symbol',s)
                rm_portf_from('symbol_list','symbol',s)
            cr.close()
        connection.close()

    except Exception as e: print(e)

def rm_portf_from(table,column,s):
    try:
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'DELETE FROM '+ str(table) +' WHERE '+ column +' = "'+ str(s) +'"'
        print(sql)
        cr.execute(sql)
        connection.commit()
        cr.close()
        connection.close()
        gc.collect()
    except Exception as e: print(e)
