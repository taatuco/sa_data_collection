# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
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

sys.path.append(os.path.abspath( sett.get_path_feed() ))
from add_feed_type import *

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def set_signals_feed(s):

    feed_id = 1
    feed_type = "signals"
    add_feed_type(feed_id, feed_type)

    #Date [Today date]
    d = datetime.datetime.now()
    d = d.strftime("%Y%m%d")

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, instruments.market, instruments.w_forecast_change, sectors.sector, instruments.w_forecast_display_info, symbol_list.uid, symbol_list.disabled, instruments.romad_st FROM instruments "+\
    "JOIN sectors ON instruments.sector = sectors.id JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol = '"+ s +"' AND instruments.symbol NOT LIKE '"+ get_portf_suffix() +"%' "

    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        symbol = row[0]
        fullname = row[1].replace("'","")
        asset_class = row[2]
        market = row[3]
        w_forecast_change = row[4]
        sector = row[5]
        w_forecast_display_info = row[6]
        uid = row[7]
        disabled = row[8]
        romad_st = row[9]

        short_title = fullname
        short_description = symbol
        content = sector
        url = "{burl}s/?uid="+ str(uid)
        ranking = str( romad_st )
        type = str(feed_id)

        if float(w_forecast_change) < 0:
            badge = "down " + w_forecast_display_info
        elif float(w_forecast_change) > 0:
            badge = "up " + w_forecast_display_info
        else:
            badge = w_forecast_display_info

        search = asset_class + market + symbol + " " + fullname

        print(search +": "+ os.path.basename(__file__) )

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM feed WHERE (symbol ='"+symbol+"' AND date<='"+d+"')"
        cr_i.execute(sql_i)
        connection.commit()

        sql_i = "INSERT INTO feed"+\
        "(date, short_title, short_description, content, url,"+\
            " ranking, symbol, type, badge, "+\
        "search, asset_class, market) "+\
        "VALUES ('"+d+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"')"
        try:
            if not disabled:
                cr_i.execute(sql_i)
                connection.commit()
        except:
            pass
        cr_i.close()
    cr.close()
