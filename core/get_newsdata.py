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

    except Exception as e: print(e)

def get_newsdata_global_rss(d,feed_id):
    try:
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT url,format,type,asset_class,market,lang FROM newsdata WHERE type="global" AND format="rss"'
        cr.execute(sql)
        rs = cr.fetchall()

        sep = ''
        insert_line = ''
        date_d = ''
        short_title = ''
        short_description = ''
        url = ''
        format = ''
        type = str(feed_id)
        search = ''
        asset_class = ''
        market = ''
        lang = ''
        #INSERT INTO feed(date, short_title, short_description, url, type, search, asset_class, market, lang)
        #VALUES ([value-1],[value-2],[value-3],[value-4],[value-5],[value-6],[value-7],[value-8],[value-9])
        for row in rs:
            url = row[0]
            feed = feedparser.parse(url)

            for post in feed.entries:
                print(post.title)
                print(post.description)
                print(post.published)

        cr.close()

    except Exception as e: print(e)
