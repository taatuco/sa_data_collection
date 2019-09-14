# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

def analyze_sentiment_of_this(text):
    r = 0
    try:
        analyser = SentimentIntensityAnalyzer()
        score = analyser.polarity_scores(text)
        data = json.loads(score)
        r = (data['compound'])
        print(str(r))
    except Exception as e: print(e)
