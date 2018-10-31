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

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

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

def get_signals(s):

    feed_id = 1
    feed_type = "signals"
    add_feed_type(feed_id, feed_type)

    #Date [Today date]
    d = datetime.datetime.now()
    d = d.strftime("%Y%m%d")

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, instruments.market, instruments.w_forecast_change, sectors.sector "+\
    "FROM instruments INNER JOIN sectors ON instruments.sector = sectors.id WHERE symbol = '"+ s +"'"

    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        symbol = row[0]
        fullname = row[1].replace("'","")
        asset_class = row[2]
        market = row[3]
        w_forecast_change = row[4]
        sector = row[5]

        short_title = symbol
        short_description = fullname + "<br>" + sector
        content = ""
        url = "signals/?s="+symbol
        ranking = str(round(w_forecast_change,5))
        type = str(feed_id)

        if (w_forecast_change < 0):
            badge = "down " + str(round(w_forecast_change*100,2))+"%"
            badge_bs_class = "badge badge-danger"
        if (w_forecast_change > 0):
            badge = "up " + str(round(w_forecast_change*100,2))+"%"
            badge_bs_class = "badge badge-success"
        if (w_forecast_change == 0):
            badge = "neutral"
            badge_bs_class = "badge badge-secondary"

        search = asset_class + market + symbol + " " + fullname

        print(search +": "+ os.path.basename(__file__) )

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "INSERT INTO feed"+\
        "(date, short_title, short_description, content, url,"+\
            " ranking, symbol, type, badge, badge_bs_class, "+\
        "search, asset_class, market) "+\
        "VALUES ('"+d+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+type+"','"+badge+"','"+badge_bs_class+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"')"
        try:
            cr_i.execute(sql_i)
            connection.commit()
        except:
            pass

        sql_i = "DELETE FROM feed WHERE (type=" + type + " AND date<'"+d+"')"
        cr_i.execute(sql_i)
        connection.commit()
