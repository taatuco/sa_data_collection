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

sql = "INSERT IGNORE INTO newsdata(name, url, format, type, asset_class, market, lang, cat) VALUES "+\
"('Reuters Company News','http://feeds.reuters.com/reuters/companyNews','rss', 'global','','','en',0), "+\
"('Reuters Business News','http://feeds.reuters.com/reuters/businessNews','rss','global','','','en',0), "+\
"('Reuters World News','http://feeds.reuters.com/Reuters/worldNews','rss','global','','','en',0), "+\
"('Yahoo Finance Global','https://finance.yahoo.com/rss/topstories','rss','global','','','en',0), "+\
"('Yahoo Finance News','https://feeds.finance.yahoo.com/rss/2.0/headline?s={yahoo_finance}','rss','specific','','','en',1), "+\
"('CNBC Top News','https://www.cnbc.com/id/100003114/device/rss/rss.html','rss','global','','','en',0), "+\
"('CNBC World News','https://www.cnbc.com/id/100727362/device/rss/rss.html','rss','global','','','en',0), "+\
"('Bing News','https://www.bing.com/news/search?q={instrument_fullname}&format=rss','rss','specific','','','en',2), "+\
"('Bing News Desc','https://www.bing.com/news/search?q={instrument_description}&format=rss','rss','specific','','','en',1), "+\
"('Google News','https://news.google.com/rss/search?q={instrument_fullname}','rss','specific','','','en',1), "+\
"('Google News Desc','https://news.google.com/rss/search?q={instrument_description}','rss','specific','','','en',1), "+\
"('Seeking Alpha Global News','https://seekingalpha.com/market_currents.xml','rss','global','EQ:','','en',0), "+\
"('Investing.com News','https://www.investing.com/rss/news_285.rss','rss','global','','','en',0), " +\
"('Investing.com Stocks News','https://www.investing.com/rss/news_25.rss','rss','global','EQ:','','en',0), "+\
"('Investing.com Crypto News','https://www.investing.com/rss/news_301.rss','rss','global','CR:','','en',0), "+\
"('Investing.com Forex News','https://www.investing.com/rss/news_1.rss','rss','global','FX:','','en',0), "+\
"('FXEmpire News','https://www.fxempire.com/api/v1/en/articles/rss/news','rss','global','FX:','','en',0), "+\
"('Daily Forex','https://www.dailyforex.com/rss/forexnews.xml','rss','global','FX:','','en',0), "+\
"('Forex Live','https://www.forexlive.com/feed/news','rss','global','FX:','','en',0), "+\
"('DailyFX News','https://rss.dailyfx.com/feeds/forex_market_news','rss','global','FX:','','en',0), "+\
"('DailyFX Daily Briefing','https://rss.dailyfx.com/feeds/daily_briefings','rss','global','FX:','','en',0), "+\
"('DailyFX Forecast','https://rss.dailyfx.com/feeds/forecasts','rss','global','FX:','','en',0), "+\
"('Realtime Forex News','https://www.realtimeforex.com/rss/','rss','global','FX:','','en',0), "+\
"('Cointelegraph All News','https://cointelegraph.com/rss','rss','global','CR:','','en',0), "+\
"('Cointelegraph Altcoin News','https://cointelegraph.com/rss/tag/altcoin','rss','global','CR:','','en',0), "+\
"('Cointelegraph Bitcoin News','https://cointelegraph.com/rss/tag/bitcoin','rss','global','CR:','','en',0), "+\
"('Cointelegraph Ethereum News','https://cointelegraph.com/rss/tag/ethereum','rss','global','CR:','','en',0), "+\
"('Cointelegraph Litecoin News','https://cointelegraph.com/rss/tag/litecoin','rss','global','CR:','','en',0), "+\
"('Cointelegraph Monero News','https://cointelegraph.com/rss/tag/monero','rss','global','CR:','','en',0), "+\
"('Coindesk News','http://feeds.feedburner.com/CoinDesk','rss','global','CR:','','en',0), "+\
"('Bitcoin com News','https://news.bitcoin.com/feed/','rss','global','CR:','','en',0), "+\
"('Minegate News','https://minergate.com/blog/feed/','rss','global','CR:','','en',0), "+\
"('NewsBTC','https://www.newsbtc.com/feed/','rss','global','CR:','','en',0), "+\
"('CryptoNinja','https://www.cryptoninjas.net/feed/','rss','global','CR:','','en',0), "+\
"('WalletInvestor','https://walletinvestor.com/blog/feed/','rss','global','CR:','','en',0), "+\
"('Finance Magnates','https://www.financemagnates.com/cryptocurrency/feed/','rss','global','CR:','','en',0), "+\
"('Bitcoin Magazine','https://bitcoinmagazine.com/feed','rss','global','CR:','','en',0)"
debug(sql +": "+ os.path.basename(__file__) )

try:
    cr.execute(sql)
    connection.commit()
    cr.close()
except Exception as e: debug(e)
