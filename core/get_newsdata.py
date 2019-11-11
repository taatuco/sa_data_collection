""" Collect news data, import into database """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import gc
import datetime
from datetime import timedelta
import feedparser
import pymysql.cursors
from get_sentiment_score import analyze_sentiment_of_this
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

sys.path.append(os.path.abspath(SETT.get_path_feed()))
from add_feed_type import add_feed_type

def get_newsdata(limit, clear_history, what, cat):
    """
    Collect news data from provided source.
    Args:
        Integer: the maximum number of news to collect.
        Boolean: if it's True, older records will be removed.
        String: Type of feed to collect, "global" or "specific" to symbol
        Integer: Category to scan where 0 means all available categories.
    Returns:
        None
    """
    #---------------------------------------------------------------------------
    # limit = max number of post to scan and collect
    # clear_history = if True then clear older records from the database
    # what = the type of feed, "global" or "specific"
    # cat = the category to scan, if 0 means all of the category will be collected
    #---------------------------------------------------------------------------
    d = datetime.datetime.now()
    dn = datetime.datetime.now() - timedelta(days=1)
    dh = datetime.datetime.now() - timedelta(days=200)
    d = d.strftime("%Y-%m-%d %H:%M:%S")
    dn = dn.strftime("%Y%m%d")
    dh = dh.strftime("%Y%m%d")

    feed_id = 3
    feed_type = "news"
    add_feed_type(feed_id, feed_type)
    get_newsdata_rss(d, feed_id, limit, what, cat)
    if clear_history: clear_old_newsdata(dh, feed_id)

def get_newsdata_rss(d, feed_id, limit, what, cat):
    """
    Collect news from rss format
    Args:
        String: date in string format YYYYMMDD
        Integer: Feed id for news data
        Integer: The maximum number of post to collect
        String: Type of feed to collect, "global", "specific"
        Integer: Category to scan where 0 means all available categories.
    Returns:
        None
    """
    filtercat = ''
    if cat > 0:
        filtercat = ' AND cat=' + str(cat)

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT url,format,type,asset_class,market,lang FROM newsdata WHERE format="rss"' + filtercat
    cr.execute(sql)
    rs = cr.fetchall()

    for row in rs:
        feed_url = row[0]
        feed_type = row[2]
        asset_class = row[3]
        market = row[4]
        lang = row[5]
        if feed_type == str('global') and (what == 'all' or what == 'global'):
            get_rss_global(feed_id, d, feed_url, asset_class, market, lang, limit)
        if feed_type == str('specific') and (what == 'all' or what == 'specific'):
            get_rss_specific(feed_id, d, feed_url, lang, limit)
    cr.close()
    connection.close()

def get_rss_global(feed_id, date_d, feed_url, asset_class, market, lang, limit):
    """
    Get news in rss format global.
    Args:
        Integer: Feed id for news data
        String: Date in string format YYYYMMDD
        String: Feed url
        String: Asset class id
        String: Market id
        String: Langugage id
        Integer: Maximum of posts to collect
    Returns:
        None
    """
    feed = feedparser.parse(feed_url)
    insert_line = ''
    short_title = ''
    short_description = ''
    url = ''
    search = ''
    sep = ''
    insert_line = ''
    sentiment_score = 0
    i = 1
    for post in feed.entries:
        short_title = str(post.title).replace("'","`")
        try:
            short_description = str(post.description).replace("'","`") + ' '+ str(post.published)
        except:
            short_description = str(post.published)

        url = str(post.link)
        search = url
        sentiment_score = analyze_sentiment_of_this(short_title+' '+short_description)

        if i > 1: sep=','
        insert_line = insert_line + sep +\
        '(\''+ str(date_d)+'\',\''+str(short_title)+'\',\''+str(short_description)+'\',\''+\
        str(url)+'\',\''+str(feed_id)+'\',\''+str(search)+'\',\''+str(asset_class)+'\',\''+str(market)+'\',\''+str(lang)+'\','+ str(sentiment_score) +')'

        if i >= limit: break
        i += 1

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'INSERT IGNORE INTO feed(date, short_title, short_description, '+\
    'url, type, search, asset_class, market, lang, ranking) VALUES '+ insert_line
    debug(sql +": "+ os.path.basename(__file__) )
    cr.execute(sql)
    connection.commit()
    gc.collect()
    cr.close()
    connection.close()

def get_rss_specific(feed_id,date_d,feed_url,lang,limit):
    """
    Get news in rss format specific to symbol.
    Args:
        Integer: Feed id for news data
        String: Date in string format YYYYMMDD
        String: Feed url
        String: Asset class id
        String: Market id
        String: Langugage id
        Integer: Maximum of posts to collect
    Returns:
        None
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)    
    cr_s = connection.cursor(pymysql.cursors.SSCursor)
    sql_s = 'SELECT instruments.asset_class, instruments.market, '+\
    'symbol_list.symbol, symbol_list.yahoo_finance, symbol_list.seekingalpha, instruments.fullname, instruments.description '+\
    'FROM symbol_list JOIN instruments ON symbol_list.symbol = instruments.symbol '+\
    'WHERE symbol_list.disabled=0 AND (symbol_list.seekingalpha<>"" OR symbol_list.yahoo_finance<>"") ORDER BY symbol'
    cr_s.execute(sql_s)
    rs = cr_s.fetchall()

    for row in rs:
        asset_class = row[0]
        market = row[1]
        symbol = row[2]
        yahoo_finance = row[3]
        seekingalpha = row[4]
        feed = ''
        instrument_fullname = row[5].replace(' ','+').replace('.','').replace(',','')
        instrument_description = row[5].replace(' ','+').replace('.','').replace(',','')
        feed_url_selection = feed_url.replace('{seekingalpha}', seekingalpha)
        feed_url_selection = feed_url_selection.replace('{yahoo_finance}', yahoo_finance)
        feed_url_selection = feed_url_selection.replace('{instrument_fullname}', instrument_fullname)
        feed_url_selection = feed_url_selection.replace('{instrument_description}', instrument_description)

        if instrument_description != '' or instrument_description is not None:
            feed = feedparser.parse(feed_url_selection)

        debug(feed_url_selection)

        insert_line = ''
        short_title = ''
        short_description = ''
        url = ''
        search = ''
        sep = ''
        insert_line = ''
        sentiment_score = 0
        i = 1
        for post in feed.entries:
            short_title = str(post.title).replace("'","`")
            try:
                short_description = str(post.description).replace("'","`") + ' '+ str(post.published)
            except:
                short_description = str(post.published)

            url = str(post.link)
            search = url
            sentiment_score = analyze_sentiment_of_this(short_title+' '+short_description)

            if i > 1: sep = ','
            insert_line = insert_line + sep +\
            '(\''+ str(date_d)+'\',\''+str(short_title)+'\',\''+str(short_description)+'\',\''+\
            str(url)+'\',\''+str(feed_id)+'\',\''+str(search)+'\',\''+str(asset_class)+'\',\''+str(market)+'\',\''+str(lang)+'\',\''+\
            str(symbol)+'\','+ str(sentiment_score) + ')'

            if i >= limit: break
            i += 1

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'INSERT IGNORE INTO feed(date, short_title, short_description, '+\
        'url, type, search, asset_class, market, lang, symbol, ranking) VALUES '+ insert_line
        debug(sql +": "+ os.path.basename(__file__) )
        cr.execute(sql)
        connection.commit()
        gc.collect()
        cr.close()
    cr_s.close()
    connection.close()

def clear_old_newsdata(dh,feed_id):
    """
    Delete news older than the threshold provided
    Args:
        String: date in string format YYYYMMDD. News older will be removed.
        Integer: Feed id that represents news
    Returns:
        None
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)    
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'DELETE FROM feed WHERE type='+ str(feed_id) + ' AND date < '+ str(dh)
    debug(sql)
    cr.execute(sql)
    connection.commit()
    gc.collect()
    cr.close()
    connection.close()
