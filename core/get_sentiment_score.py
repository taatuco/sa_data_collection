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


def analyze_sentiment_of_this(text):
    r = 0
    try:
        analyser = SentimentIntensityAnalyzer()
        score = analyser.polarity_scores(text)
        r = (score.get('compound'))
        print(str(r))
    except Exception as e: print(e)
    return r

def get_sentiment_score_avg(s,dh):
    r = 0
    try:
        last_row_id = 0
        avg_sentiment = 0
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT id FROM price_data_instruments WHERE symbol="'+ str(s) +'" ORDER BY id DESC LIMIT 1'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: last_row_id = row[0]

        sql = 'SELECT AVG(ranking) FROM feed WHERE symbol="'+ str(s) +'" AND type=3 AND date>='+ str(dh)
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: avg_sentiment = row[0]
        cr.close()

    except Exception as e: print(e)
    return r
