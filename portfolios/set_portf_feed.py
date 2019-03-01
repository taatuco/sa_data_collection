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

def get_portf_content(user_id):
    r = ''
    try:
        nickname = ''
        avatar_id = ''
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT nickname, avatar_id FROM users WHERE id="+ str(user_id)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: nickname = row[0]; avatar_id = row[1]
        r = '<img src="{burl}static/avatar/'+ str(avatar_id) +'.png" style="vertical-align: middle;border-style: none;width: 30px;">&nbsp;<strong>'+nickname+'</strong>'
    except Exception as e: print(e)
    return r

def set_portf_feed():

    feed_id = 9
    feed_type = "portfolios"
    add_feed_type(feed_id, feed_type)

    #Date [Today date]
    d = datetime.datetime.now()
    d = d.strftime("%Y%m%d")

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, instruments.market, instruments.w_forecast_change, instruments.w_forecast_display_info, symbol_list.uid, instruments.owner, instruments.romad_st FROM instruments "+\
    "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol LIKE '"+ get_portf_suffix() +"%' AND y1 > 0"

    cr.execute(sql)
    rs = cr.fetchall()
    i = 0
    inserted_value = ''
    for row in rs:
        symbol = row[0]
        fullname = row[1].replace("'","")
        asset_class = row[2]
        market = row[3]
        w_forecast_change = row[4]
        w_forecast_display_info = row[5]
        uid = row[6]
        owner = row[7]
        romad_st = row[8]

        short_title = fullname
        short_description = symbol
        content = get_portf_content(owner)
        url = "{burl}p/?uid="+str(uid)
        ranking = str( romad_st )
        type = str(feed_id)

        badge = w_forecast_display_info
        search = asset_class + market + symbol + " " + fullname
        print(search +": "+ os.path.basename(__file__) )

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_value = inserted_value + sep +\
        "('"+d+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"')"

        i += 1

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM feed WHERE (symbol = '"+ symbol+"' AND date<='"+d+"')"
        cr_i.execute(sql_i)
        connection.commit()

    sql_i = "INSERT IGNORE INTO feed"+\
    "(date, short_title, short_description, content, url,"+\
        " ranking, symbol, type, badge, "+\
    "search, asset_class, market) VALUES " + inserted_value
    print(sql_i)
    try:
        cr_i.execute(sql_i)
        connection.commit()
    except Exception as e:
        print(e + ' ' + os.path.basename(__file__) )
        pass
    cr_i.close()


    cr.close()
