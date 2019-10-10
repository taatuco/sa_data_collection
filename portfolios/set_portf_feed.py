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

sys.path.append(os.path.abspath( sett.get_path_feed() ))
from add_feed_type import *

from pathlib import Path

import pymysql.cursors

def get_portf_content(user_id):
    r = ''
    try:
        nickname = ''
        avatar_id = ''
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT nickname, avatar_id FROM users WHERE id="+ str(user_id)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: nickname = row[0]; avatar_id = row[1]
        r = '<img src="{burl}static/avatar/'+ str(avatar_id) +'.png" style="vertical-align: middle;border-style: none;width: 30px;">&nbsp;<strong>'+nickname+'</strong>'
        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def get_portf_ranking(s,rank,stdev_st,y1,m6,m3,m1):
    r = 0
    try:
        count_negative_year = 0
        count_blown_portf = 0
        max_drawdown_reached = False
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol FROM instruments WHERE symbol ='"+ s +"' AND y1<=0 "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: count_negative_year = 1

        sql = "SELECT symbol FROM chart_data WHERE symbol ='"+ s +"' AND price_close <= 0 "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: count_blown_portf = 1

        account_start = 1000
        sql = "SELECT account_reference FROM instruments WHERE symbol='"+ s +"'"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: account_start = row[0]

        drawdown_pct_threshold = 0.3
        drawdown_account_max = float(account_start) - (float(account_start) * float(drawdown_pct_threshold) )
        sql = "SELECT price_close FROM chart_data WHERE symbol ='"+ s +"' AND price_close < "+ str(drawdown_account_max) + " LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: max_drawdown_reached = True

        r = float(rank)
        #Negative monthly return
        if float(rank) <= 0:
            r = r - 9999
        #Rank down negative year
        if count_negative_year > 0:
            r = float(rank) - 500
        else:
            if max_drawdown_reached:
                r = r - 999
            #Rank up yearly performance
            if float(y1) > 0.05:
                r = r + 500
            if float(y1) > 0.09:
                r = r + 900
            #Rank up 6-month performance
            if float(m6) > 0.05:
                r = r + 500
            if float(m6) > 0.09:
                r = r + 900
            #Rank up 3-month performance
            if float(m3) > 0.05:
                r = r + 500
            if float(m3) > 0.09:
                r = r + 900
            #Rank up 1-month performance
            if float(m1) > 0.05:
                r = r + 1000
            if float(m1) > 0.09:
                r = r + 2000

        #Rank down blown portfolio
        if count_blown_portf > 0:
            r = float(rank) - 999999

        cr.close()
        connection.close()
    except Exception as e: print(e)
    return r

def set_portf_feed():

    feed_id = 9
    feed_type = "portfolios"
    add_feed_type(feed_id, feed_type)

    #Date [Today date]
    d = datetime.datetime.now()
    d = d.strftime("%Y%m%d")
    connection = pymysql.connect(host=db_srv,
                                 user=db_usr,
                                 password=db_pwd,
                                 db=db_name,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, instruments.market, instruments.w_forecast_change, "+\
    "instruments.w_forecast_display_info, symbol_list.uid, instruments.owner, "+\
    "instruments.romad_st, instruments.stdev_st, instruments.y1, instruments.m6, instruments.m3, instruments.m1 "+\
    "FROM instruments "+\
    "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol LIKE '"+ get_portf_suffix() +"%'"

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
        stdev_st = row[9]
        y1 = row[10]
        m6 = row[11]
        m3 = row[12]
        m1 = row[13]

        short_title = fullname
        short_description = symbol
        content = get_portf_content(owner)
        url = "{burl}p/?uid="+str(uid)
        ranking =  str( get_portf_ranking(symbol, romad_st, stdev_st,y1,m6,m3,m1) )
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

    i = 1
    d = datetime.datetime.now() ; d = d.strftime('%Y%m')

    portf_symbol = ''
    cr_r = connection.cursor(pymysql.cursors.SSCursor)
    sql_r = "SELECT feed.symbol, instruments.creation_date FROM feed JOIN instruments ON feed.symbol = instruments.symbol WHERE feed.type = 9 AND instruments.creation_date < "+d+"01 ORDER BY feed.ranking DESC"
    cr_r.execute(sql_r)
    rs_r = cr_r.fetchall()
    for row in rs_r:
        portf_symbol = row[0]
        cr_u = connection.cursor(pymysql.cursors.SSCursor)
        sql_u = "UPDATE feed SET globalRank = "+ str(i) + " WHERE symbol = '"+ str(portf_symbol) +"'"
        print(sql_u)
        cr_u.execute(sql_u)
        i += 1
        connection.commit()
        gc.collect()
    cr_r.close()
    cr.close()
    connection.close()
