""" Set and generate strategy portfolio feed """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import gc
import datetime
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, get_portf_suffix, debug, get_hash_string
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()
sys.path.append(os.path.abspath(SETT.get_path_feed()))
from add_feed_type import add_feed_type

def get_portf_content(user_id):
    """
    Get strategy portfolio content for the feed.Return the nickname and
    avatar of the owner of the portfolio.
    Args:
        Int: User id
    Returns:
        String: Nickname and avatar in html format
    """
    ret = ''
    nickname = ''
    avatar_id = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT nickname, avatar_id FROM users WHERE id="+ str(user_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        nickname = row[0]
        avatar_id = row[1]
    ret = '<img src="{burl}static/avatar/'+ str(avatar_id) +'.png" '+\
    'style="vertical-align: middle;border-style: none;width: 30px;">&nbsp;<strong>'+\
    nickname+'</strong>'
    cursor.close()
    connection.close()
    return ret

def get_portf_ranking(symbol, rank, y1_performance, m6_performance, m3_performance, m1_performance):
    """
    Rank portfolio based on various criteria such as maximum drawdown,
    negative year, month, etc...
    Args:
        String: Symbol of the portfolio
        Double: Return on max drawdown (RoMAD) is used to rank
        Double: 1-year strategy portfolio performance
        Double: 6-month strategy portfolio performance
        Double: 3-month strategy portfolio performance
        Double: 1-month strategy portfolio performance
    Returns:
        None
    """
    ret = 0
    count_negative_year = 0
    count_blown_portf = 0
    max_drawdown_reached = False
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol FROM instruments WHERE symbol ='"+ symbol +"' AND y1<=0 "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        count_negative_year = 1

    sql = "SELECT symbol FROM chart_data WHERE symbol ='"+ symbol +"' AND price_close <= 0 "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        count_blown_portf = 1

    account_start = 1000
    sql = "SELECT account_reference FROM instruments WHERE symbol='"+ symbol +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        account_start = row[0]

    drawdown_pct_threshold = 0.3
    drawdown_account_max = (float(account_start) * float(drawdown_pct_threshold))
    drawdown_account_max = float(account_start) - drawdown_account_max
    sql = "SELECT price_close FROM chart_data WHERE symbol ='"+ symbol +\
    "' AND price_close < "+ str(drawdown_account_max) + " LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        max_drawdown_reached = True

    ret = float(rank)
    #Negative return on max drawdown
    if float(rank) <= 0:
        ret = ret - 9999
    #Rank down negative year
    if count_negative_year > 0:
        ret = float(rank) - 500
    else:
        if max_drawdown_reached:
            ret = ret - 999
        #Rank up yearly performance
        if float(y1_performance) > 0.05:
            ret = ret + 500
        if float(y1_performance) > 0.09:
            ret = ret + 900
        #Rank up 6-month performance
        if float(m6_performance) > 0.05:
            ret = ret + 500
        if float(m6_performance) > 0.09:
            ret = ret + 900
        #Rank up 3-month performance
        if float(m3_performance) > 0.05:
            ret = ret + 500
        if float(m3_performance) > 0.09:
            ret = ret + 900
        #Rank up 1-month performance
        if float(m1_performance) > 0.05:
            ret = ret + 1000
        if float(m1_performance) > 0.09:
            ret = ret + 2000

    #Rank down blown portfolio
    if count_blown_portf > 0:
        ret = float(rank) - 999999

    cursor.close()
    connection.close()
    return ret

def set_portf_feed():
    """
    Import all the portfolio to table feed.
    Args:
        None
    Returns:
        None
    """
    feed_id = 9
    feed_type = "portfolios"
    add_feed_type(feed_id, feed_type)

    #Date [Today date]
    date_today = datetime.datetime.now()
    date_today = date_today.strftime("%Y%m%d")
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cr_i = connection.cursor(pymysql.cursors.SSCursor)
    sql_i = "DELETE FROM feed WHERE type= "+ str(feed_id)
    cr_i.execute(sql_i)
    connection.commit()


    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, "+\
    "instruments.market, instruments.w_forecast_change, "+\
    "instruments.w_forecast_display_info, symbol_list.uid, instruments.owner, "+\
    "instruments.romad_st, instruments.stdev_st, instruments.y1, instruments.m6, "+\
    "instruments.m3, instruments.m1 "+\
    "FROM instruments "+\
    "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol LIKE '"+ get_portf_suffix() +"%'"

    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    inserted_value = ''
    for row in res:
        symbol = row[0]
        fullname = row[1].replace("'", "")
        asset_class = row[2]
        market = row[3]
        w_forecast_display_info = row[5]
        uid = row[6]
        owner = row[7]
        romad_st = row[8]
        y1_performance = row[10]
        m6_performance = row[11]
        m3_performance = row[12]
        m1_performance = row[13]

        short_title = fullname
        short_description = symbol
        content = get_portf_content(owner)
        url = "{burl}p/?uid="+str(uid)
        ranking = str(get_portf_ranking(symbol, romad_st, y1_performance,
                                        m6_performance, m3_performance, m1_performance))
        feed_type = str(feed_id)
        hash_this = get_hash_string(str(url))

        badge = w_forecast_display_info
        search = asset_class + market + symbol + " " + fullname
        debug(search +": "+ os.path.basename(__file__))

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_value = inserted_value + sep +\
        "('"+date_today+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market +"','"+hash_this+"'" +")"

        i += 1

    sql_i = "INSERT IGNORE INTO temp_feed"+\
    "(date, short_title, short_description, content, url,"+\
        " ranking, symbol, type, badge, "+\
    "search, asset_class, market, hash) VALUES " + inserted_value
    debug(sql_i)
    cr_i.execute('''CREATE TEMPORARY TABLE temp_feed
    SELECT * FROM feed
    LIMIT 0;''')
    cr_i.execute(sql_i)
    connection.commit()
    cr_i.execute('SELECT @i := 0')
    cr_i.execute('UPDATE temp_feed SET globalRank = (SELECT @i := @i +1) ORDER BY ranking DESC')
    connection.commit()
    cr_i.execute('INSERT INTO feed SELECT * FROM temp_feed')
    connection.commit()

    cr_i.close()
    gc.collect()
    cursor.close()
    connection.close()
