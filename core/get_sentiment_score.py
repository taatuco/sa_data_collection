# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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
import pymysql.cursors

def analyze_sentiment_of_this(text):
    r = 0
    try:
        analyser = SentimentIntensityAnalyzer()
        score = analyser.polarity_scores(text)
        r = (score.get('compound'))
        debug(str(r))
    except Exception as e: debug(e)
    return r

def get_sentiment_score_avg(s,dh):
    r = 0
    try:
        avg_sentiment = 0
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT AVG(ranking) FROM feed WHERE symbol="'+ str(s) +'" AND type=3 AND date>='+ str(dh)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: avg_sentiment = row[0]
        cr.close()
        connection.close()
        r = avg_sentiment
    except Exception as e: debug(e)
    return r
