""" Text sentiment analysis """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import pymysql.cursors
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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

def analyze_sentiment_of_this(text):
    """
    Provide a sentiment score from a given text.
    Args:
        String: text to evaluate sentiment
    Returns:
        Double: Sentiment score
    """
    ret = 0
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(text)
    ret = (score.get('compound'))
    debug(str(ret))
    return ret

def get_sentiment_score_avg(symbol, date_greater_than):
    """
    From the feed table, get an average sentiment of the specified instrument.
    Args:
        String: Symbol of the instrument
        String: Date in string format
    Returns:
        None
    """
    ret = 0
    avg_sentiment = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT AVG(ranking) FROM feed WHERE symbol="'+\
    str(symbol) +'" AND type=3 AND date>='+ str(date_greater_than)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        avg_sentiment = row[0]
    cursor.close()
    connection.close()
    if avg_sentiment is not None:
        ret = avg_sentiment
    return ret
