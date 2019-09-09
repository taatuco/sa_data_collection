# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cr = connection.cursor(pymysql.cursors.SSCursor)

sql = "INSERT IGNORE INTO newsdata(name, url, format, type, asset_class, market, lang) VALUES "+\
"('Reuters Company News','http://feeds.reuters.com/reuters/companyNews','rss', 'global','','','en'), "+\
"('Reuters Business News','http://feeds.reuters.com/reuters/businessNews','rss','global','','','en'), "+\
"('Reuters World News','http://feeds.reuters.com/Reuters/worldNews','rss','global','','','en'), "+\
"('Yahoo Finance Global','https://finance.yahoo.com/rss/topstories','rss','global','','','en'), "+\
"('Yahoo Finance News','https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}','rss','specific','','','en'), "+\
"('CNBC Top News','https://www.cnbc.com/id/100003114/device/rss/rss.html','rss','global','','','en'), "+\
"('CNBC World News','https://www.cnbc.com/id/100727362/device/rss/rss.html','rss','global','','','en'), "+\
"('Yahoo News','https://news.yahoo.com/rss','rss','global','','','en'), "+\
"('Seeking Alpha News','https://seekingalpha.com/api/sa/combined/{symbol}.xml','rss','specific','','','en'), "+\
"('Seeking Alpha Global News','https://seekingalpha.com/market_currents.xml','rss','global','EQ:','','en'), "+\
"('Investing.com News','https://www.investing.com/rss/news_285.rss','rss','global','','','en'), " +\
"('Investing.com Stocks News','https://www.investing.com/rss/news_25.rss','rss','global','EQ:','','en') "+\
"('Investing.com Crypto News','https://www.investing.com/rss/news_301.rss','rss','global','CR:','','en') "+\
"('Investing.com Forex News','https://www.investing.com/rss/news_1.rss','rss','global','FX:','','en') "+\
"('FXEmpire News','https://www.fxempire.com/api/v1/en/articles/rss/news','rss','global','FX:','','en') "+\
"('Daily Forex','https://www.dailyforex.com/rss/forexnews.xml','rss','global','FX:','','en') "+\
"('Forex Live','https://www.forexlive.com/feed/news','rss','global','FX:','','en') "+\
"('DailyFX News','https://rss.dailyfx.com/feeds/forex_market_news','rss','global','FX:','','en') "+\
"('DailyFX Daily Briefing','https://rss.dailyfx.com/feeds/daily_briefings','rss','global','FX:','','en') "+\
"('DailyFX Forecast','https://rss.dailyfx.com/feeds/forecasts','rss','global','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "+\
"('','','','','','','en') "

print(sql +": "+ os.path.basename(__file__) )

try:
    cr.execute(sql)
    connection.commit()
    cr.close()
except Exception as e: print(e)
