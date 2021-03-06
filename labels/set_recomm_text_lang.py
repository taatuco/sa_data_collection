""" Import recommendation text into the database """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_product_name
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def set_recomm_text_lang():
    """
    Import recommendationt text template into the database
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

    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "DELETE FROM recommendations"
    cr.execute(sql)
    connection.commit()

    ######## English ########
    lang_en = "en"
    price_under_200ma_en = "The price is currently below the 200-day average, "+\
    "which indicates a downward pressure on {symbol} to further decline in the longer term."

    price_above_200ma_en = "The price is currently above the 200-day average, "+\
    "which indicates an upward pressure on {symbol} to further rally in the longer term."

    st_upper_range_above_price_range_en = "The near term upper range is at {st_upper_range} "+\
    "above the last daily closing. At that level, sellers might rush to cover their "+\
    "positions leading to a possible retest of the near-term lower range "+\
    "before in continues with the rally."

    st_lower_range_below_price_range_en = "The near term lower range is at {st_lower_range} "+\
    "below the last daily closing. At that level, buyers might be interested "+\
    "to buy more, leading to higher price potential."

    upper_range_below_price_downtrend_en = "{symbol} break out through the near "+\
    "term upper range at {st_upper_range}. {symbol} might be temporarily overbought, "+\
    "which could result in a correction in price accordingly."

    lower_range_above_price_uptrend_en = "{symbol} break below the near term lower range "+\
    "at {st_lower_range}. We are estimating that {symbol} might be "+\
    "temporarily oversold, which could see a rebound in price."

    rsi_oversold_en = "According to the Relative Strength Index, on a 50-day average basis, "+\
    "{symbol} might be in an oversold territory that indicates that "+\
    "there is possible reversal in price pattern."

    rsi_overbought_en = "According to the Relative Strength Index, on a 50-day average basis, "+\
    "{symbol} might be in an overbought territory. A potential retracement "+\
    "could be seen with a high chance of at least a correction on the "+\
    "previous support that may see further decline in price."

    rsi_weak_en = "According to the Relative Strength Index, on a 50-day average basis, "+\
    "{symbol} relative strength in price action remains weak at an average {rsi_50_day_avg}. "+\
    "It is advised to be cautious of the price inconsistency."

    rsi_strong_en = "According to the Relative Strength Index, on a 50-day average basis, "+\
    "{symbol} relative strength in price action remains strong at an average {rsi_50_day_avg}. "+\
    "Accordingly, a further positive momentum could be anticipated."

    uptrend_recomm_en = "{symbol} in the near term is technically positive. "+\
    "An opportunistic buy with an entry below {buy_entry} with a primary "+\
    "target at {buy_target_price} is recommended. On the other hand, above {sell_entry} "+\
    "a sell opportunity could be considered with a stop loss set at "+\
    "{sell_stop_loss} and target price at {sell_target_price}."

    downtrend_recomm_en = "{symbol} in the near term is technically negative. "+\
    "An opportunistic sell with an entry above {sell_entry} with a primary target "+\
    "at {sell_target_price} is recommended. On the other hand, below {buy_entry} "+\
    "a buy opportunity could be considered with a stop loss set "+\
    "at {buy_stop_loss} and target price at {buy_target_price}."

    portf_descr_en = "As per the "+ get_product_name() +" proprietary algorithm, "+\
    "projected profit of up to {display_forecast} for every {account_minimum} {unit} "+\
    "invested is achievable within the next 7 days with the following allocation: {portf_recomm} "+\
    "The specified portfolio has achieved an aggregated profit/loss of {portf_last_price} {unit} "+\
    "in the last 12 months with as a reference a trading account of {account_minimum} {unit}."

    portf_recomm_buy_en = "buy {portf_alloc_instr} below {portf_alloc_entry_price}"

    portf_recomm_sell_en = "sell {portf_alloc_instr} above {portf_alloc_entry_price}"

    portf_risk_consider_en = "With a {account_reference} {unit} trading account as reference, "+\
    "there is a potential risk that the portfolio get exposed to a {dollar_amount} {unit} "+\
    "loss according to the last 30 days price pattern. In percentage terms, "+\
    "the portfolio can be affected to a {percentage} volatility."

    sql = "INSERT IGNORE INTO recommendations(lang, price_under_200ma, price_above_200ma, "+\
    "st_upper_range_above_price_range, st_lower_range_below_price_range, "+\
    "upper_range_below_price_downtrend, lower_range_above_price_uptrend, "+\
    "rsi_oversold, rsi_overbought, rsi_weak, rsi_strong, "+\
    "uptrend_recomm, downtrend_recomm, portf_descr, portf_recomm_buy, portf_recomm_sell, "+\
    "portf_risk_consider) VALUES "+\
    "('"+lang_en+"', '"+price_under_200ma_en+"', '"+price_above_200ma_en+"', "+\
    "'"+st_upper_range_above_price_range_en+"', '"+st_lower_range_below_price_range_en+\
    "', '"+upper_range_below_price_downtrend_en+"', "+\
    "'"+lower_range_above_price_uptrend_en+"', '"+rsi_oversold_en+"', '"+\
    rsi_overbought_en+"', '"+rsi_weak_en+"', "+\
    "'"+rsi_strong_en+"', '"+uptrend_recomm_en+"', '"+downtrend_recomm_en+\
    "', '"+portf_descr_en+"', '"+portf_recomm_buy_en+ "', '"+portf_recomm_sell_en+"', "+\
    "'"+portf_risk_consider_en+"'"  +")"
    debug(sql)
    cr.execute(sql)
    connection.commit()
    cr.close()
    connection.close()

set_recomm_text_lang()
