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
sql = "DELETE FROM briefing"
cr.execute(sql)
connection.commit()


######## English ########
#{keyword}
lang_en = "en"
_1_worldstocks_day_up_week_down = 'Stocks climbed by {day_percent} on {yesterday} after declining by {week_percent} since last week.'
_1_worldstocks_day_down_week_up = 'Stocks felt by {day_percent} on {yesterday} after advancing by {week_percent} since last week.'
_2_worldstocks_day_up_week_up = 'Stocks continue to climb by {day_percent} on {yesterday} reinforcing its upside by {week_percent} since last week.'
_2_worldstocks_day_down_week_down = 'Stocks continue to decline by {day_percent} on {yesterday} contributing to a loss of {week_percent} since last week.'
_3_worldstocks_day_up_ma10_down = 'Despite the Global Stock Market closed higher, it prevails under the 10-day average which could suggest some limitations in further gains in the near-term.'
_3_worldstocks_day_down_ma10_up = 'Despite the Global Stock Market closed lower, it resides above the 10-day average which could suggest a likely near-term rebound.'
_4_worldstocks_day_up_ma10_up = 'As the Global Stock Market is closing higher and evolving above its 10-day average exhibits a certain optimism that could lead the Equity Market in the near-term to extend its bullish momentum.'
_4_worldstocks_day_down_ma10_down = 'As the Global Stock Market is closing lower and evolving below its 10-day average unveils a certain deterioration of confidence that could lead the Equity Market in the near-term to extend its bearish momentum.'
_5_vix_day_up_week_down = 'Volatility is increasing by {day_percent} expressing a growing uncertainty from the investors, yet, confidence is somehow preserved as shown by the Volatility Index trending down for a week.'
_5_vix_day_down_week_down = 'Volatility decreased by {day_percent} expressing investors\' confidence in risk assets. The Volatility Index is trending down for a week suggesting momentarily optimism in the stock market.'
_6_vix_day_up_week_up = 'Volatility progress by {day_percent} since {yesterday} attesting a continuation of investors\' confidence deterioration since last week.'
_6_vix_day_down_week_up = 'Volatility decreased by {day_percent} showing a return of investors\' confidence in the Equity Market since last week.'
_7_worldstocks_up_JPY_down = 'The Yen depreciated against the US dollar as risk appetite improves, prompting investors to abandon the safe-haven currency.'
_7_worldstocks_down_JPY_down = 'The Yen depreciated against the US dollar as investors might regain confidence and urged to abandon the safe-haven currency to seek higher returns in riskier assets.'
_8_workdstocks_up_JPY_up = 'The Yen progressed by {day_percent} against the US dollar.'
_8_worldstocks_down_JPY_up = 'The Yen advanced by {day_percent} against the US dollar as investors seek refuge in the safe-haven currency.'
_9_gold_up = 'Gold benefited, up {day_percent}.'
_9_gold_down = 'Gold lost {day_percent}.'
_10_BTC_day_up_week_up = 'Bitcoin is posting some gains with upside at {day_percent} adding up to a {week_percent} since last week.'
_10_BTC_day_down_week_up = 'Bitcoin is posting some losses with {day_percent}, however, it remained in the upside for a week, up {week_percent}.'
_11_BTC_day_up_week_down = 'Bitcoin is posting some gains with {day_percent}, but still in the downside since a week, down {week_percent}.'
_11_BTC_day_down_week_down = 'Bitcoin is posting continuous losses down {day_percent} and {week_percent} since a week.'

sql = 'INSERT IGNORE INTO briefing'+\
'(_1_worldstocks_day_up_week_down,_1_worldstocks_day_down_week_up,_2_worldstocks_day_up_week_up,_2_worldstocks_day_down_week_down,'+\
'_3_worldstocks_day_up_ma10_down,_3_worldstocks_day_down_ma10_up,_4_worldstocks_day_up_ma10_up,_4_worldstocks_day_down_ma10_down,'+\
'_5_vix_day_up_week_down,_5_vix_day_down_week_down,_6_vix_day_up_week_up,_6_vix_day_down_week_up,'+\
'_7_worldstocks_up_JPY_down,_7_worldstocks_down_JPY_down,_8_workdstocks_up_JPY_up,_8_worldstocks_down_JPY_up,'+\
'_9_gold_up,_9_gold_down,_10_BTC_day_up_week_up,_10_BTC_day_down_week_up,_11_BTC_day_up_week_down,_11_BTC_day_down_week_down) VALUES '+\
'("'+_1_worldstocks_day_up_week_down+'","'+_1_worldstocks_day_down_week_up+'","'+_2_worldstocks_day_up_week_up+'","'+_2_worldstocks_day_down_week_down+'","'+\
_3_worldstocks_day_up_ma10_down+'","'+_3_worldstocks_day_down_ma10_up+'","'+_4_worldstocks_day_up_ma10_up+'","'+_4_worldstocks_day_down_ma10_down+'","'+\
_5_vix_day_up_week_down+'","'+_5_vix_day_down_week_down+'","'+_6_vix_day_up_week_up+'","'+_6_vix_day_down_week_up+'","'+_7_worldstocks_up_JPY_down+'","'+\
_7_worldstocks_down_JPY_down+'","'+_8_workdstocks_up_JPY_up+'","'+_8_worldstocks_down_JPY_up+'","'+_9_gold_up,_9_gold_down+'","'+_10_BTC_day_up_week_up+'","'+\
_10_BTC_day_down_week_up+'","'+_11_BTC_day_up_week_down+'","'+_11_BTC_day_down_week_down+'")'

print(sql)

try:
    cr.execute(sql)
    connection.commit()
except Exception as e: print(e)

cr.close()
connection.close()
