# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
import time
import feedparser

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_feed() ))
from add_feed_type import *

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

def get_newsdata():
    try:

        #Date [Today date]
        d = datetime.datetime.now()
        d = d.strftime("%Y%m%d")

        feed_id = 3
        feed_type = "news"
        add_feed_type(feed_id, feed_type)
        get_newsdata_rss(d,feed_id)

    except Exception as e: print(e)

def get_newsdata_rss(d,feed_id):
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT url,format,type,asset_class,market,lang FROM newsdata WHERE format="rss"'
        cr.execute(sql)
        rs = cr.fetchall()

        for row in rs:
            feed_url = row[0]
            format = row[1]
            type = row[2]
            asset_class = row[3]
            market = row[4]
            lang = row[5]

            if type == str('global'):
                get_rss_global(feed_id,d,feed_url,asset_class,market,lang)
            if type == str('specific'):
                get_rss_specific(feed_id,d,feed_url,asset_class,market,lang)

        cr.close()

    except Exception as e: print(e)

def get_rss_global(feed_id,date_d,feed_url,asset_class,market,lang):
    try:
        feed = feedparser.parse(feed_url)
        insert_line = ''
        short_title = ''
        short_description = ''
        url = ''
        search = ''
        i = 1
        for post in feed.entries:
            short_title = str(post.title).replace("'","`")
            try:
                short_description = str(post.description).replace("'","`") + ' '+ str(post.published)
            except:
                short_description = str(post.published)

            url = str(post.link)
            search = url
            cr = connection.cursor(pymysql.cursors.SSCursor)
            sql = 'INSERT IGNORE INTO feed(date, short_title, short_description, '+\
            'url, type, search, asset_class, market, lang) VALUES '+\
            '(\''+ str(date_d)+'\',\''+str(short_title)+'\',\''+str(short_description)+'\',\''+\
            str(url)+'\',\''+str(feed_id)+'\',\''+str(search)+'\',\''+str(asset_class)+'\',\''+str(market)+'\',\''+str(lang)+'\')'
            cr.execute(sql)
            connection.commit()
            print(sql +": "+ os.path.basename(__file__) )

            i += 1
        cr.close()

    except Exception as e: print(s)

def get_rss_specific(feed_id,date_d,feed_url,asset_class,market,lang):
    try:

        cr_s = connection.cursor(pymysql.cursors.SSCursor)
        sql_s = 'SELECT symbol, yahoo_finance, seekingalpha FROM symbol_list WHERE disabled=0 AND seekingalpha<>"" OR yahoo_finance<>"" ORDER BY symbol'
        cr_s.execute(sql_s)
        rs = cr_s.fetchall()

        for row in rs:
            yahoo_finance = row[0]
            seekingalpha = row[1]
            feed_url_selection = feed_url.replace('{seekingalpha}', seekingalpha)
            feed_url_selection = feed_url.replace('{yahoo_finance}', yahoo_finance)
            feed = feedparser.parse(feed_url_selection)
            print(feed_url_selection)

            insert_line = ''
            short_title = ''
            short_description = ''
            url = ''
            search = ''
            i = 1
            for post in feed.entries:
                short_title = str(post.title).replace("'","`")
                try:
                    short_description = str(post.description).replace("'","`") + ' '+ str(post.published)
                except:
                    short_description = str(post.published)

                url = str(post.link)
                search = url
                cr = connection.cursor(pymysql.cursors.SSCursor)
                sql = 'INSERT IGNORE INTO feed(date, short_title, short_description, '+\
                'url, type, search, asset_class, market, lang) VALUES '+\
                '(\''+ str(date_d)+'\',\''+str(short_title)+'\',\''+str(short_description)+'\',\''+\
                str(url)+'\',\''+str(feed_id)+'\',\''+str(search)+'\',\''+str(asset_class)+'\',\''+str(market)+'\',\''+str(lang)+'\')'
                cr.execute(sql)
                connection.commit()
                print(sql +": "+ os.path.basename(__file__) )
                i += 1
                cr.close()

        cr_s.close()

    except Exception as e: print(e)