""" Import text for market briefing and various market reports into db """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import pymysql.cursors
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


def set_briefing_text_lang():
    """
    Import text for the market briefing and various market reports in each
    of the available languages, into the database.
    Args:
        None
    Returns:
        None
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "DELETE FROM briefing"
    cursor.execute(sql)
    connection.commit()


    ######## English ########
    #{keyword}
    lang_en = "en"

    txt_1_worldstocks_day_up_week_down_en = 'Stocks climbed by {day_percent} '+\
    'on previous session after declining by {week_percent} since last week.'

    txt_1_worldstocks_day_down_week_up_en = 'Stocks felt by {day_percent} '+\
    'on previous session after advancing by {week_percent} since last week.'

    txt_2_worldstocks_day_up_week_up_en = 'Stocks continue to climb by {day_percent} '+\
    'on previous session reinforcing its upside by {week_percent} since last week.'

    txt_2_worldstocks_day_down_week_down_en = 'Stocks continue to decline by {day_percent} '+\
    'on previous session contributing to a loss of {week_percent} since last week.'

    txt_3_worldstocks_day_up_ma10_down_en = 'Despite the Global Stock Market closed higher, '+\
    'it prevails under the 10-day average which could suggest some '+\
    'limitations in further gains in the near-term.'

    txt_3_worldstocks_day_down_ma10_up_en = 'Despite the Global Stock Market closed lower, '+\
    'it resides above the 10-day average which could suggest a likely near-term rebound.'

    txt_4_worldstocks_day_up_ma10_up_en = 'As the Global Stock Market is closing higher '+\
    'and evolving above its 10-day average exhibits a certain optimism that could lead '+\
    'the Equity Market in the near-term to extend its bullish momentum.'

    txt_4_worldstocks_day_down_ma10_down_en = 'As the Global Stock Market is closing lower '+\
    'and evolving below its 10-day average unveils a certain deterioration of confidence '+\
    'that could lead the Equity Market in the near-term to extend its bearish momentum.'

    txt_5_vix_day_up_week_down_en = 'Volatility is increasing by {day_percent} '+\
    'expressing a growing uncertainty from the investors, yet, confidence is somehow preserved '+\
    'as shown by the Volatility Index trending down for a week.'

    txt_5_vix_day_down_week_down_en = 'Volatility decreased by {day_percent} '+\
    'expressing investors\' confidence in risk assets. The Volatility Index '+\
    'is trending down for a week suggesting momentarily optimism in the stock market.'

    txt_6_vix_day_up_week_up_en = 'Volatility progress by {day_percent} '+\
    'since previous session attesting a continuation of '+\
    'investors\' confidence deterioration since last week.'

    txt_6_vix_day_down_week_up_en = 'Volatility decreased by {day_percent} '+\
    'showing a return of investors\' confidence in the Equity Market since last week.'

    txt_7_worldstocks_up_jpy_down_en = 'The Yen depreciated against the US dollar '+\
    'as risk appetite improves, prompting investors to abandon the safe-haven currency.'

    txt_7_worldstocks_down_jpy_down_en = 'The Yen depreciated against the US dollar '+\
    'as investors might regain confidence and urged to abandon the safe-haven '+\
    'currency to seek higher returns in riskier assets.'

    txt_8_workdstocks_up_jpy_up_en = 'The Yen progressed by {day_percent} against the US dollar.'

    txt_8_worldstocks_down_jpy_up_en = 'The Yen advanced by {day_percent} '+\
    'against the US dollar as investors seek refuge in the safe-haven currency.'

    txt_9_gold_up_en = 'Gold benefited, up {day_percent}.'

    txt_9_gold_down_en = 'Gold lost {day_percent}.'

    txt_10_btc_day_up_week_up_en = 'Bitcoin is posting some gains with upside '+\
    'at {day_percent} adding up to a {week_percent} since last week.'

    txt_10_btc_day_down_week_up_en = 'Bitcoin is posting some losses with {day_percent}, '+\
    'however, it remained in the upside for a week, up {week_percent}.'

    txt_11_btc_day_up_week_down_en = 'Bitcoin is posting some gains with {day_percent}, '+\
    'but still in the downside since a week, down {week_percent}.'

    txt_11_btc_day_down_week_down_en = 'Bitcoin is posting continuous losses down '+\
    '{day_percent} and {week_percent} since a week.'

    sql = 'INSERT IGNORE INTO briefing'+\
    '(lang,_1_worldstocks_day_up_week_down,_1_worldstocks_day_down_week_up,'+\
    '_2_worldstocks_day_up_week_up,_2_worldstocks_day_down_week_down,'+\
    '_3_worldstocks_day_up_ma10_down,_3_worldstocks_day_down_ma10_up,'+\
    '_4_worldstocks_day_up_ma10_up,_4_worldstocks_day_down_ma10_down,'+\
    '_5_vix_day_up_week_down,_5_vix_day_down_week_down,_6_vix_day_up_week_up,'+\
    '_6_vix_day_down_week_up,'+\
    '_7_worldstocks_up_JPY_down,_7_worldstocks_down_JPY_down,'+\
    '_8_workdstocks_up_JPY_up,_8_worldstocks_down_JPY_up,'+\
    '_9_gold_up,_9_gold_down,_10_BTC_day_up_week_up,_10_BTC_day_down_week_up,'+\
    '_11_BTC_day_up_week_down,_11_BTC_day_down_week_down) VALUES '+\
    '("'+ lang_en  +'","'+txt_1_worldstocks_day_up_week_down_en+'","'+\
    txt_1_worldstocks_day_down_week_up_en+'","'+txt_2_worldstocks_day_up_week_up_en+'","'+\
    txt_2_worldstocks_day_down_week_down_en+'","'+\
    txt_3_worldstocks_day_up_ma10_down_en+'","'+txt_3_worldstocks_day_down_ma10_up_en+'","'+\
    txt_4_worldstocks_day_up_ma10_up_en+'","'+txt_4_worldstocks_day_down_ma10_down_en+'","'+\
    txt_5_vix_day_up_week_down_en+'","'+txt_5_vix_day_down_week_down_en+\
    '","'+txt_6_vix_day_up_week_up_en+'","'+\
    txt_6_vix_day_down_week_up_en+'","'+txt_7_worldstocks_up_jpy_down_en+'","'+\
    txt_7_worldstocks_down_jpy_down_en+'","'+txt_8_workdstocks_up_jpy_up_en+'","'+\
    txt_8_worldstocks_down_jpy_up_en+'","'+txt_9_gold_up_en+'","'+txt_9_gold_down_en+'","'+\
    txt_10_btc_day_up_week_up_en+'","'+\
    txt_10_btc_day_down_week_up_en+'","'+txt_11_btc_day_up_week_down_en+\
    '","'+txt_11_btc_day_down_week_down_en+'")'

    debug(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()


set_briefing_text_lang()
