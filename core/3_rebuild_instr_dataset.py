# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import gc
import time
import datetime
from datetime import timedelta

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

sys.path.append(os.path.abspath( sett.get_path_core() ))
from ta_instr_sum import *
from get_sentiment_score import *

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def rebuild_instr_dataset():

    sql_parse_list = "SELECT symbol_list.symbol, symbol_list.uid, instruments.asset_class "+\
    "FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol  WHERE symbol_list.symbol NOT LIKE '"+get_portf_suffix()+"%' AND symbol_list.disabled = 0 ORDER BY symbol"

    import pymysql.cursors
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = sql_parse_list
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            s = row[0]
            uid = row[1]
            asset_class = row[2]
            cr_pip = connection.cursor(pymysql.cursors.SSCursor)
            sql_pip = "SELECT pip FROM instruments WHERE symbol ='"+ s +"' "
            cr_pip.execute(sql_pip)
            rs_pip = cr_pip.fetchall()
            for row in rs_pip:
                pip = row[0]
            cr_pip.close()

            print(str(uid) + ' - ' + str(s) + '------------------------------' )
            print(s +": "+ str(pip) +": "+ os.path.basename(__file__) )
            dn = datetime.datetime.now() - timedelta(days=10)
            dn = dn.strftime("%Y%m%d")
            dh = datetime.datetime.now() - timedelta(days=7)
            dh = dh.strftime("%Y%m%d")
            d = datetime.datetime.now() - timedelta(days=370)
            d = d.strftime("%Y%m%d")
            sentiment = 0

            sql_select_instr = "SELECT id, date FROM price_instruments_data WHERE (symbol='"+s+"' and date>"+d+") ORDER BY date ASC"
            cr_d_id = connection.cursor(pymysql.cursors.SSCursor)
            sql_d_id = sql_select_instr
            cr_d_id.execute(sql_d_id)
            rs_d = cr_d_id.fetchall()
            for row in rs_d: sentiment = get_sentiment_score_avg(s,dh)

            get_instr_sum(s,uid,asset_class,dn,pip,sentiment)

        cr.close()

    finally:
        connection.close()
