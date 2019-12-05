""" Functionalities related to Instrument signals and feed """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_portf_suffix, get_hash_string
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_feed()))
from add_feed_type import add_feed_type, set_feed_function
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def get_signal_ranking(symbol, rank):
    """
    Get signal rank from monthly signal performance
    Args:
        String: instrument symbol
        Double: performance in percentage or pips
    Returns:
        Double: rank in percentage
    """
    ret = 0
    unit = ''
    divider = 1
    pip_divider = 10000
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT unit FROM instruments WHERe symbol = '"+ symbol +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        unit = row[0]

    if unit == 'pips':
        divider = pip_divider

    ret = float(rank) / divider


    cursor.close()
    connection.close()
    return ret

def set_signals_feed(symbol, connection):
    """
    Import instrument signals in table feed
    Args:
        String: Instrument symbol
    Returns:
        None
    """
    feed_id = 1
    feed_type = "signals"
    add_feed_type(feed_id, feed_type)

    #Date [Today date]
    date_today = datetime.datetime.now()
    date_today = date_today.strftime("%Y%m%d")

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT instruments.symbol, instruments.fullname, instruments.asset_class, "+\
    "instruments.market, instruments.w_forecast_change, sectors.sector, "+\
    "instruments.w_forecast_display_info, symbol_list.uid, "+\
    "instruments.m1_signal FROM instruments "+\
    "JOIN sectors ON instruments.sector = sectors.id JOIN symbol_list ON "+\
    "instruments.symbol = symbol_list.symbol "+\
    "WHERE instruments.symbol = '"+ symbol +"' AND instruments.symbol NOT LIKE '"+\
    get_portf_suffix() +"%' AND symbol_list.disabled=0"

    cursor.execute(sql)
    res = cursor.fetchall()
    i = 0
    inserted_values = ''
    for row in res:
        symbol = row[0]
        fullname = row[1].replace("'", "")
        asset_class = row[2]
        market = row[3]
        w_forecast_change = row[4]
        sector = row[5]
        w_forecast_display_info = row[6]
        uid = row[7]
        m1_signal = row[8]

        short_title = fullname
        short_description = symbol
        content = sector
        url = "{burl}s/?uid="+ str(uid)
        ranking = str(get_signal_ranking(symbol, m1_signal))
        feed_type = str(feed_id)
        hash_this = get_hash_string(str(url))

        if float(w_forecast_change) < 0:
            badge = '<i class="fas fa-caret-down"></i>&nbsp;' + w_forecast_display_info
        elif float(w_forecast_change) > 0:
            badge = '<i class="fas fa-caret-up"></i>&nbsp;' + w_forecast_display_info
        else:
            badge = w_forecast_display_info

        search = set_feed_function('DES', symbol, 'label') +\
        asset_class + market + " " + fullname + ' - ' + 'Security Tearsheet'

        sa_function = set_feed_function('DES', symbol, 'value')

        debug(search +": "+ os.path.basename(__file__))

        cr_d = connection.cursor(pymysql.cursors.SSCursor)
        sql_d = "DELETE FROM feed WHERE (symbol ='"+symbol+"' AND date<='"+\
        date_today+"' AND type="+ feed_type +")"
        cr_d.execute(sql_d)
        connection.commit()

        if i == 0:
            sep = ''
        else:
            sep = ','
        inserted_values = inserted_values + sep +\
        "('"+date_today+"','"+short_title+"','"+short_description+"','"+content+"','"+url+"',"+\
        "'"+ranking+"','"+symbol+"','"+feed_type+"','"+badge+"',"+\
        "'"+search+"','"+asset_class+"','"+market+"','"+sa_function+"','"+hash_this+"'"+")"

        cr_d.close()
    cursor.close()

    cr_i = connection.cursor(pymysql.cursors.SSCursor)

    sql_i = "INSERT IGNORE INTO feed"+\
    "(date, short_title, short_description, content, url,"+\
    " ranking, symbol, type, badge, "+\
    "search, asset_class, market, sa_function, hash) VALUES " + inserted_values
    cr_i.execute(sql_i)
    connection.commit()
    cr_i.close()
