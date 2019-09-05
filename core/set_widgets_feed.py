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

def set_widgets_feed(s):
    try:
        feed_id = 2
        feed_type = "widgets"
        add_feed_type(feed_id, feed_type)

        set_widgets_tradingview_chart(s,feed_id)
        set_widgets_from_url(feed_id,'Tradebook','{burl}w/?funcname=get_trades_box(0,burl,1)','TB: Tradebook')
        set_widgets_from_url(feed_id,'My Portfolio(s)','{burl}ls/?w=portf','PORT: List of my Portfolio(s)')
        set_widgets_from_url(feed_id,'Dashboard','{burl}?dashboard=1','DASH: Dashboard - All relevant info in One place')
        set_widgets_from_url(feed_id,'All Signals','{burl}ls/?w=instr&x=','SIGNAL:GO> All Trading Signals')
        set_widgets_from_url(feed_id,'FX Signals','{burl}ls/?w=instr&x=FX:','SIGNAL:FX:GO> Forex Trading Signals')
        set_widgets_from_url(feed_id,'All Stocks Signals','{burl}ls/?w=instr&x=EQ:','SIGNAL:EQ: All stocks Trading Signals')
        set_widgets_from_url(feed_id,'Crypto Signals','{burl}ls/?w=instr&x=CR:','SIGNAL:CR:GO> Cryptocurrency Trading Signals')
        set_widgets_from_url(feed_id,'Economic Calendar','{burl}w/?funcname=get_tradingview_ecocal(0,0)','ECOCAL:GO> Economic Calendar')

    except Exception as e: print(e)

def set_widgets_from_url(feed_id,short_title,url,search):
    try:
        d = datetime.datetime.now()
        d = d.strftime("%Y%m%d")
        short_description = short_title
        content = short_title
        ranking = '-1'
        symbol = ''
        type = str(feed_id)
        badge = ''
        asset_class = '-'
        market = '-'

        cr_i = connection.cursor(pymysql.cursors.SSCursor)


        inserted_values = " " +\
        "('"+d+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"')"


        sql_i = "INSERT IGNORE INTO feed"+\
        "(date, short_title, short_description, content, url,"+\
        " ranking, symbol, type, badge, "+\
        "search, asset_class, market) VALUES " + inserted_values
        try:
            cr_i.execute(sql_i)
            connection.commit()
        except:
            pass
        cr_i.close()
    except Exception as e: print(e)

def set_widgets_tradingview_chart(s,feed_id):

    #Date [Today date]
    d = datetime.datetime.now()
    d = d.strftime("%Y%m%d")

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, instruments.market, sectors.sector, symbol_list.uid, symbol_list.disabled FROM instruments "+\
    "JOIN sectors ON instruments.sector = sectors.id JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol = '"+ s +"' AND instruments.symbol NOT LIKE '"+ get_portf_suffix() +"%' "

    cr.execute(sql)
    rs = cr.fetchall()
    i = 0
    inserted_values = ''
    for row in rs:
        symbol = row[0]
        fullname = row[1].replace("'","")
        asset_class = row[2]
        market = row[3]
        sector = row[4]
        uid = row[5]
        disabled = row[6]

        short_title = fullname
        short_description = symbol
        content = sector
        url = "{burl}w/?funcname=get_tradingview_chart("+ str(uid) +",0,0)"
        badge = ''
        ranking = '-1'
        type = str(feed_id)
        search = "CHART:" + symbol + " " + fullname

        print(search +": "+ os.path.basename(__file__) )

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM feed WHERE (symbol ='"+symbol+"' AND date<='"+d+"' AND type="+ type +")"
        cr_i.execute(sql_i)
        connection.commit()

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_values = inserted_values + sep +\
        "('"+d+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"')"

    cr.close()

    sql_i = "INSERT IGNORE INTO feed"+\
    "(date, short_title, short_description, content, url,"+\
    " ranking, symbol, type, badge, "+\
    "search, asset_class, market) VALUES " + inserted_values
    try:
        if not disabled:
            cr_i.execute(sql_i)
            connection.commit()
    except:
        pass
        cr_i.close()
