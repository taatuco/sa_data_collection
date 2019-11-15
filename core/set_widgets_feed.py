""" Functionalities related to widgets """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_portf_suffix, get_hash_string
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_feed()))
from add_feed_type import add_feed_type
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def set_widgets_feed(symbol):
    """
    Set widget feed. Create widget from a URL
    Args:
        String: Instrument symbol
    Returns:
        None
    """
    feed_id = 2
    feed_type = "widgets"
    add_feed_type(feed_id, feed_type)
    set_widgets_tradingview_chart(symbol, feed_id)

    set_widgets_from_url(feed_id,
                         'FX Heatmap',
                         '{burl}w/?funcname=get_tradingview_fxheatmap(0,0)',
                         'FX:GO>HM: Forex Heat Map')
    set_widgets_from_url(feed_id,
                         'Tradebook',
                         '{burl}w/?funcname=get_trades_box(0,burl,1)',
                         'TB: Tradebook')
    set_widgets_from_url(feed_id,
                         'Dashboard',
                         '{burl}?dashboard=1',
                         'DASH: Dashboard - All relevant info in One place')
    set_widgets_from_url(feed_id,
                         'Top Portfolios',
                         '{burl}ls/?w=portf&x=',
                         'TOPPORT: Traders Top Portfolios')
    set_widgets_from_url(feed_id,
                         'All Signals',
                         '{burl}ls/?w=instr&x=',
                         'SIGNAL:GO> All Trading Signals')
    set_widgets_from_url(feed_id,
                         'FX Signals',
                         '{burl}ls/?w=instr&x=FX:',
                         'SIGNAL:FX:GO> Forex Trading Signals')
    set_widgets_from_url(feed_id,
                         'All Stocks Signals',
                         '{burl}ls/?w=instr&x=EQ:',
                         'SIGNAL:EQ: All stocks Trading Signals')
    set_widgets_from_url(feed_id,
                         'U.S. Stocks Signals',
                         '{burl}ls/?w=instr&x=US>',
                         'SIGNAL:EQ:US> U.S. stocks Trading Signals')
    set_widgets_from_url(feed_id,
                         'Crypto Signals',
                         '{burl}ls/?w=instr&x=CR:',
                         'SIGNAL:CR:GO> Cryptocurrency Trading Signals')
    set_widgets_from_url(feed_id,
                         'Economic Calendar',
                         '{burl}w/?funcname=get_tradingview_ecocal(0,0)&refreshw=1800',
                         'ECOCAL:GO> Economic Calendar')
    set_widgets_from_url(feed_id,
                         'World News and Top Stories',
                         '{burl}w/?funcname=get_newsfeed(burl,0,0,500,1)&refreshw=900&noflexheight=1',
                         'TOP:GO> World News and Top Stories')


def set_widgets_from_url(feed_id, short_title, url, search):
    """
    Insert into table feed widget from an url
    Args:
        String: id of feed type that identify a widget
        String: Short title of the widget
        String: URL to link to the widget
        String: Search caption
    Returns:
        None
    """
    date_today = datetime.datetime.now()
    date_today = date_today.strftime("%Y%m%d")
    short_description = short_title
    content = short_title
    ranking = '-1'
    symbol = ''
    feed_type = str(feed_id)
    badge = ''
    asset_class = '-'
    market = '-'
    hash_this = get_hash_string(str(url))

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr_i = connection.cursor(pymysql.cursors.SSCursor)


    inserted_values = " " +\
    "('"+date_today+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
    "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
    "'"+search+"','"+asset_class+"','"+market+"','"+hash_this+"'"+"')"


    sql_i = "INSERT IGNORE INTO feed"+\
    "(date, short_title, short_description, content, url,"+\
    " ranking, symbol, type, badge, "+\
    "search, asset_class, market) VALUES " + inserted_values
    cr_i.execute(sql_i)
    connection.commit()
    cr_i.close()
    connection.close()

def set_widgets_tradingview_chart(symbol, feed_id):
    """
    Create tradingview chart widget for each symbol as per args
    Args:
        String: Instrument symbol
        Integer: Id of feed type to identfy as widget
    Returns:
        None
    """
    date_today = datetime.datetime.now()
    date_today = date_today.strftime("%Y%m%d")

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, "+\
    "instruments.asset_class, instruments.market, sectors.sector, "+\
    "symbol_list.uid, symbol_list.disabled FROM instruments "+\
    "JOIN sectors ON instruments.sector = sectors.id JOIN symbol_list ON "+\
    "instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol = '"+ symbol +"' AND instruments.symbol NOT LIKE '"+\
    get_portf_suffix() +"%' "

    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    inserted_values = ''
    for row in res:
        symbol = row[0]
        fullname = row[1].replace("'", "")
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
        feed_type = str(feed_id)
        search = "CHART:" + symbol + " " + fullname
        hash_this = get_hash_string(str(url))

        debug(search +": "+ os.path.basename(__file__))

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM feed WHERE (symbol ='"+symbol+"' AND date<='"+\
        date_today+"' AND type="+ type +")"
        cr_i.execute(sql_i)
        connection.commit()

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_values = inserted_values + sep +\
        "('"+date_today+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"','"+hash_this+"'"+")"

        cr_i.close()
    cursor.close()

    cr_i = connection.cursor(pymysql.cursors.SSCursor)
    sql_i = "INSERT IGNORE INTO feed"+\
    "(date, short_title, short_description, content, url,"+\
    " ranking, symbol, type, badge, "+\
    "search, asset_class, market, hash) VALUES " + inserted_values
    if not disabled:
        cr_i.execute(sql_i)
        connection.commit()

    cr_i.close()
    connection.close()
