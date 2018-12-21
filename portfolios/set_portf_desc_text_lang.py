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

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def set_recomm_text_lang():

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "DELETE FROM recommendations"
    cr.execute(sql)
    connection.commit()


    ######## English ########
    lang_en = "en"
    price_under_200ma_en ="The price is currently below the 200-day average, which indicates a downward pressure on {symbol} to further decline in the longer term"
    price_above_200ma_en ="The price is currently above the 200-day average, which indicates an upward pressure on {symbol} to further rally in the longer term"
    st_upper_range_above_price_range_en ="The near term upper range is at {st_upper_range} above the last daily closing. At that level, sellers might rush to cover their positions leading to a possible retest of the near-term lower range before in continues with the rally."
    st_lower_range_below_price_range_en ="The near term lower range is at {st_lower_range} below the last daily closing. At that level, buyers might be interested to buy more, leading to higher price potential."
    upper_range_below_price_downtrend_en ="{symbol} break out through the near term upper range at {st_upper_range}. {symbol} might be temporarily overbought, which could result in a correction in price accordingly."
    lower_range_above_price_uptrend_en ="{symbol} break below the near term lower range at {st_lower_range}. We are estimating that {symbol} might be temporarily oversold, which could see a rebound in price."
    rsi_oversold_en ="According to the Relative Strength Index, on a 50-day average basis, {symbol} might be in an oversold territory that indicates that there is possible reversal in price pattern."
    rsi_overbought_en ="According to the Relative Strength Index, on a 50-day average basis, {symbol} might be in an overbought territory. A potential retracement could be seen with a high chance of at least a correction on the previous support that may see further decline in price."
    rsi_weak_en ="According to the Relative Strength Index, on a 50-day average basis, {symbol} relative strength in price action remains weak at an average {rsi_50_day_avg}. It is advised to be cautious of the price inconsistency."
    rsi_strong_en ="According to the Relative Strength Index, on a 50-day average basis, {symbol} relative strength in price action remains strong at an average {rsi_50_day_avg}. Accordingly, a further positive momentum could be anticipated."
    uptrend_recomm_en ="{symbol} in the near term is technically positive. An opportunistic buy with an entry below {buy_entry} with a primary target at {buy_target_price} is recommended. On the other hand, above {sell_entry} a sell opportunity could be considered with a stop loss set at {sell_stop_loss} and target price at {sell_target_price}."
    downtrend_recomm_en ="{symbol} in the near term is technically negative. An opportunistic sell with an entry above {sell_entry} with a primary target at {sell_target_price} is recommended. On the other hand, below {buy_entry} a buy opportunity could be considered with a stop loss set at {buy_stop_loss} and target price at {buy_target_price}."



    sql = "INSERT INTO recommendations(lang, price_under_200ma, price_above_200ma, "+\
    "st_upper_range_above_price_range, st_lower_range_below_price_range, "+\
    "upper_range_below_price_downtrend, lower_range_above_price_uptrend, "+\
    "rsi_oversold, rsi_overbought, rsi_weak, rsi_strong, "+\
    "uptrend_recomm, downtrend_recomm) VALUES "+\
    "('"+lang_en+"', '"+price_under_200ma_en+"', '"+price_above_200ma_en+"', "+\
     "'"+st_upper_range_above_price_range_en+"', '"+st_lower_range_below_price_range_en+"', '"+upper_range_below_price_downtrend_en+"', "+\
     "'"+lower_range_above_price_uptrend_en+"', '"+rsi_oversold_en+"', '"+rsi_overbought_en+"', '"+rsi_weak_en+"', "+\
     "'"+rsi_strong_en+"', '"+uptrend_recomm_en+"', '"+downtrend_recomm_en+"')"

    try:
        cr.execute(sql)
        connection.commit()
    except Exception as e: print(e)
