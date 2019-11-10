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
from settings import SmartAlphaPath, get_portf_suffix, debug
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
    Desc
    Args:
        None
    Returns:
        None
    """
    r = ''
    nickname = ''
    avatar_id = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT nickname, avatar_id FROM users WHERE id="+ str(user_id)
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: nickname = row[0]; avatar_id = row[1]
    r = '<img src="{burl}static/avatar/'+ str(avatar_id) +'.png" '+\
    'style="vertical-align: middle;border-style: none;width: 30px;">&nbsp;<strong>'+\
    nickname+'</strong>'
    cr.close()
    connection.close()
    return r

def get_portf_ranking(s, rank, y1, m6, m3, m1):
    """
    Desc
    Args:
        None
    Returns:
        None
    """
    r = 0
    count_negative_year = 0
    count_blown_portf = 0
    max_drawdown_reached = False
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol FROM instruments WHERE symbol ='"+ s +"' AND y1<=0 "
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: count_negative_year = 1

    sql = "SELECT symbol FROM chart_data WHERE symbol ='"+ s +"' AND price_close <= 0 "
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: count_blown_portf = 1

    account_start = 1000
    sql = "SELECT account_reference FROM instruments WHERE symbol='"+ s +"'"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: account_start = row[0]

    drawdown_pct_threshold = 0.3
    drawdown_account_max = (float(account_start) * float(drawdown_pct_threshold))
    drawdown_account_max = float(account_start) - drawdown_account_max
    sql = "SELECT price_close FROM chart_data WHERE symbol ='"+ s +\
    "' AND price_close < "+ str(drawdown_account_max) + " LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs: max_drawdown_reached = True

    r = float(rank)
    #Negative monthly return
    if float(rank) <= 0:
        r = r - 9999
    #Rank down negative year
    if count_negative_year > 0:
        r = float(rank) - 500
    else:
        if max_drawdown_reached:
            r = r - 999
        #Rank up yearly performance
        if float(y1) > 0.05:
            r = r + 500
        if float(y1) > 0.09:
            r = r + 900
        #Rank up 6-month performance
        if float(m6) > 0.05:
            r = r + 500
        if float(m6) > 0.09:
            r = r + 900
        #Rank up 3-month performance
        if float(m3) > 0.05:
            r = r + 500
        if float(m3) > 0.09:
            r = r + 900
        #Rank up 1-month performance
        if float(m1) > 0.05:
            r = r + 1000
        if float(m1) > 0.09:
            r = r + 2000

    #Rank down blown portfolio
    if count_blown_portf > 0:
        r = float(rank) - 999999

    cr.close()
    connection.close()
    return r

def set_portf_feed():
    """
    Desc
    Args:
        None
    Returns:
        None
    """
    feed_id = 9
    feed_type = "portfolios"
    add_feed_type(feed_id, feed_type)

    #Date [Today date]
    d = datetime.datetime.now()
    d = d.strftime("%Y%m%d")
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


    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, "+\
    "instruments.market, instruments.w_forecast_change, "+\
    "instruments.w_forecast_display_info, symbol_list.uid, instruments.owner, "+\
    "instruments.romad_st, instruments.stdev_st, instruments.y1, instruments.m6, "+\
    "instruments.m3, instruments.m1 "+\
    "FROM instruments "+\
    "JOIN symbol_list ON instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol LIKE '"+ get_portf_suffix() +"%'"

    cr.execute(sql)
    rs = cr.fetchall()
    i = 0
    inserted_value = ''
    for row in rs:
        symbol = row[0]
        fullname = row[1].replace("'", "")
        asset_class = row[2]
        market = row[3]
        w_forecast_display_info = row[5]
        uid = row[6]
        owner = row[7]
        romad_st = row[8]
        y1 = row[10]
        m6 = row[11]
        m3 = row[12]
        m1 = row[13]

        short_title = fullname
        short_description = symbol
        content = get_portf_content(owner)
        url = "{burl}p/?uid="+str(uid)
        ranking = str(get_portf_ranking(symbol, romad_st, y1, m6, m3, m1))
        feed_type = str(feed_id)

        badge = w_forecast_display_info
        search = asset_class + market + symbol + " " + fullname
        debug(search +": "+ os.path.basename(__file__))

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_value = inserted_value + sep +\
        "('"+d+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"')"

        i += 1

    sql_i = "INSERT IGNORE INTO temp_feed"+\
    "(date, short_title, short_description, content, url,"+\
        " ranking, symbol, type, badge, "+\
    "search, asset_class, market) VALUES " + inserted_value
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
    cr.close()
    connection.close()
