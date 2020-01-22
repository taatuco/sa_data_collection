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
from add_feed_type import add_feed_type, set_feed_function
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def set_widgets_feed(symbol, connection):
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
    set_widgets_tradingview_chart(symbol, feed_id, connection)

    set_widgets_from_url(feed_id, connection,
                         'FX Heatmap',
                         '{burl}w/?funcname=get_tradingview_fxheatmap(0,0,1)',
                         set_feed_function('GO', 'FXC', 'label') +\
                         'Forex Heat Map',
                         set_feed_function('GO', 'FXC', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'Tradebook',
                         '{burl}w/?funcname=get_trades_box(0,burl,1)&noflexheight=1',
                         set_feed_function('GO', 'TBX', 'label') +\
                         'Tradebook',
                         set_feed_function('GO', 'TBX', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'Dashboard',
                         '{burl}?dashboard=1',
                         set_feed_function('DASH', 'PORT', 'label') +\
                         'Dashboard - All relevant info in One place',
                         set_feed_function('DASH', 'PORT', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'Top Portfolios',
                         '{burl}ls/?w=portf&x=',
                         set_feed_function('TOP', 'PORT', 'label') +\
                         'Traders Top Strategy Portfolios',
                         set_feed_function('TOP', 'PORT', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'All Signals',
                         '{burl}ls/?w=instr&x=',
                         set_feed_function('ALL', 'SIGNAL', 'label') +\
                         'All Trading Signals',
                         set_feed_function('ALL', 'SIGNAL', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'FX Signals',
                         '{burl}ls/?w=instr&x=FX:',
                         set_feed_function('FX', 'SIGNAL', 'label') +\
                         'Forex Trading Signals',
                         set_feed_function('FX', 'SIGNAL', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'All Stocks Signals',
                         '{burl}ls/?w=instr&x=EQ:',
                         set_feed_function('EQ', 'SIGNAL', 'label') +\
                         'All stocks Trading Signals',
                         set_feed_function('EQ', 'SIGNAL', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'U.S. Stocks Signals',
                         '{burl}ls/?w=instr&x=US>',
                         set_feed_function('EQ:US', 'SIGNAL', 'label') +\
                         'U.S. stocks Trading Signals',
                         set_feed_function('EQ:US', 'SIGNAL', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'Crypto Signals',
                         '{burl}ls/?w=instr&x=CR:',
                         set_feed_function('CR', 'SIGNAL', 'label') +\
                         'Cryptocurrency Trading Signals',
                         set_feed_function('CR', 'SIGNAL', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'Economic Calendar',
                         '{burl}w/?funcname=get_tradingview_ecocal(0,0,1)&refreshw=1800',
                         set_feed_function('GO', 'ECO', 'label') +\
                         'Economic Calendar',
                         set_feed_function('GO', 'ECO', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'World News and Top Stories',
                         '{burl}w/?funcname=get_newsfeed(burl,0,0,500,1,0)&refreshw=900&noflexheight=1',
                         set_feed_function('GO', 'TOP', 'label') +\
                         'World News and Top Stories',
                         set_feed_function('GO', 'TOP', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'FX',
                         '{burl}w/?funcname=get_tradingview_screener(0,0,1)',
                         set_feed_function('FX', 'EQS', 'label') +\
                         'Forex Screener',
                         set_feed_function('FX', 'EQS', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'EQ:US',
                         '{burl}w/?funcname=get_tradingview_screener(0,0,2)',
                         set_feed_function('EQ:US', 'EQS', 'label') +\
                         'U.S. Stocks Screener',
                         set_feed_function('EQ:US', 'EQS', 'value'))
    set_widgets_from_url(feed_id, connection,
                         'CR',
                         '{burl}w/?funcname=get_tradingview_screener(0,0,5)',
                         set_feed_function('CR', 'EQS', 'label') +\
                         'Cryptocurrencies Screener',
                         set_feed_function('CR', 'EQS', 'value'))    
    set_widgets_from_url(feed_id, connection,
                         'Trading Instruments Watchlist',
                         '{burl}w/?funcname=get_tradingview_watchlist(0,0,1)',
                         set_feed_function('GO', 'WATCHLIST', 'label') +\
                         'Watchlist',
                         set_feed_function('GO', 'WATCHLIST', 'value'))


def set_widgets_from_url(feed_id, connection, short_title, url, search, sa_function):
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

    cr_i = connection.cursor(pymysql.cursors.SSCursor)


    inserted_values = " " +\
    "('"+date_today+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
    "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
    "'"+search+"','"+asset_class+"','"+market+"','"+sa_function+"','"+hash_this+"'"+")"


    sql_i = "INSERT IGNORE INTO feed"+\
    "(date, short_title, short_description, content, url,"+\
    " ranking, symbol, type, badge, "+\
    "search, asset_class, market, sa_function, hash) VALUES " + inserted_values
    cr_i.execute(sql_i)
    connection.commit()
    cr_i.close()

def set_widgets_tradingview_chart(symbol, feed_id, connection):
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
    disabled = True

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
        url = "{burl}w/?funcname=get_tradingview_chart("+ str(uid) +",0,0,1)"
        badge = ''
        ranking = '-1'
        feed_type = str(feed_id)
        search = set_feed_function('GP', symbol, 'label') + fullname + ' - Interactive Chart / Historical Graphs'
        sa_function = set_feed_function('GP', symbol, 'value')
        hash_this = get_hash_string(str(url))

        debug(search +": "+ os.path.basename(__file__))

        cr_i = connection.cursor(pymysql.cursors.SSCursor)
        sql_i = "DELETE FROM feed WHERE (symbol ='"+symbol+"' AND date<='"+\
        date_today+"' AND type="+ feed_type +")"
        cr_i.execute(sql_i)
        connection.commit()

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_values = inserted_values + sep +\
        "('"+date_today+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"','"+sa_function+"','"+hash_this+"'"+")"

        cr_i.close()
    cursor.close()

    cr_i = connection.cursor(pymysql.cursors.SSCursor)
    sql_i = "INSERT IGNORE INTO feed"+\
    "(date, short_title, short_description, content, url,"+\
    " ranking, symbol, type, badge, "+\
    "search, asset_class, market, sa_function, hash) VALUES " + inserted_values
    if not disabled:
        cr_i.execute(sql_i)
        connection.commit()

    cr_i.close()
