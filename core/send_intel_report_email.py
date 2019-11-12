""" Compile and send the daily intelligence report """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
import pymysql.cursors
from send_mail import send_mail
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_reply_to_email
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def get_condition(symbol, symbol_jpy, what):
    """
    Get the technical condition for the instrument as per args
    Args:
        String: Symbol of the selected instrument
        String: Symbol related to USD Japanese Yen
        String: What condition to test
    Returns:
        String: Return a string that define the condition as per args
    """
    ret = ''
    w_1 = 0
    d_1 = 0
    ma10 = 0
    jpyd1 = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT w1, d1, unit FROM instruments WHERE symbol = "'+ str(symbol) +'" '
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        w_1 = row[0]
        d_1 = row[1]

    sql = 'SELECT w1, d1 FROM instruments WHERE symbol = "'+ str(symbol_jpy) +'" '
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        jpyd1 = row[1]*(-1)


    sql = 'SELECT ma10, price_close FROM price_instruments_data WHERE symbol = "'+\
    str(symbol) +'" ORDER BY date DESC LIMIT 1'
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ma10 = row[0]
        s_price = row[1]

    cursor.close()
    connection.close()

    if what == 'd1_w1':
        if d_1 > 0 and w_1 < 0:
            ret = 'd1_up_w1_down'
        if d_1 < 0 and w_1 > 0:
            ret = 'd1_down_w1_up'
        if d_1 > 0 and w_1 > 0:
            ret = 'd1_up_w1_up'
        if d_1 < 0 and w_1 < 0:
            ret = 'd1_down_w1_down'
    if what == 'd1_ma10':
        if d_1 > 0 and s_price < ma10:
            ret = 'd1_up_ma10_down'
        if d_1 < 0 and s_price > ma10:
            ret = 'd1_down_ma10_up'
        if d_1 > 0 and s_price > ma10:
            ret = 'd1_up_ma10_up'
        if d_1 < 0 and s_price < ma10:
            ret = 'd1_down_ma10_down'
    if what == 'd1_jpy':
        if d_1 > 0 and jpyd1 < 0:
            ret = 'd1_up_jpy_down'
        if d_1 < 0 and jpyd1 < 0:
            ret = 'd1_down_jpy_down'
        if d_1 > 0 and jpyd1 > 0:
            ret = 'd1_up_jpy_up'
        if d_1 < 0 and jpyd1 > 0:
            ret = 'd1_down_jpy_up'
    if what == 'gold':
        if d_1 > 0:
            ret = 'd1_up'
        if d_1 < 0:
            ret = 'd1_down'
    return ret

def get_perf(symbol, period, reverse):
    """
    Get performance of the instrument as per args for a selected period
    Args:
        String: Symbol of the instrument
        String: Period to measure
        Boolean: If True then reverse the calculation
    Returns:
        None
    """
    ret = ''
    w_1 = ''
    d_1 = ''
    unit = ''
    multiplier = 1
    if reverse:
        multiplier = -1

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT w1, d1, unit FROM instruments WHERE symbol = "'+ str(symbol) +'" '
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        unit = str(row[2])

        if unit == '%':
            w_1 = str(round(row[0]*100, 2)*multiplier)
            d_1 = str(round(row[1]*100, 2)*multiplier)

        if unit == 'pips':
            w_1 = str(round(row[0], 0)*multiplier)
            d_1 = str(round(row[1], 0)*multiplier)
    cursor.close()
    connection.close()

    sep = ''
    if unit != '%':
        sep = ' '
    if period == 'd1':
        ret = d_1 + sep + unit
    if period == 'w1':
        ret = w_1 + sep + unit
    return ret

def compile_market_snapshot():
    """
    Compile the market snapshot
    Args:
        None
    Returns:
        String: Text report of the market snapshot.
    """
    ret = ''
    report = ''
    language = 'en'
    symbol_worldstocks = 'NYSEARCA:URTH'
    d1_world = get_perf(symbol_worldstocks, 'd1', False)
    w1_world = get_perf(symbol_worldstocks, 'w1', False)
    symbol_vix = 'INDEXCBOE:BVZ'
    d1_vix = get_perf(symbol_vix, 'd1', False)
    w1_vix = get_perf(symbol_vix, 'w1', False)
    symbol_jpy = 'USDJPY'
    d1_jpy = get_perf(symbol_jpy, 'd1', True)
    w1_jpy = get_perf(symbol_jpy, 'w1', True)
    symbol_gold = 'GLD'
    d1_gold = get_perf(symbol_gold, 'd1', False)
    w1_gold = get_perf(symbol_gold, 'w1', False)
    symbol_btc = 'BITCOIN'
    d1_btc = get_perf(symbol_btc, 'd1', False)
    w1_btc = get_perf(symbol_btc, 'w1', False)

    day_pct = '{day_percent}'
    week_pct = '{week_percent}'

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT ' +\
    '_1_worldstocks_day_up_week_down, _1_worldstocks_day_down_week_up, '+\
    '_2_worldstocks_day_up_week_up, _2_worldstocks_day_down_week_down, '+\
    '_3_worldstocks_day_up_ma10_down, _3_worldstocks_day_down_ma10_up, '+\
    '_4_worldstocks_day_up_ma10_up, _4_worldstocks_day_down_ma10_down, '+\
    '_5_vix_day_up_week_down, _5_vix_day_down_week_down, '+\
    '_6_vix_day_up_week_up, _6_vix_day_down_week_up, '+\
    '_7_worldstocks_up_JPY_down, _7_worldstocks_down_JPY_down, '+\
    '_8_workdstocks_up_JPY_up, _8_worldstocks_down_JPY_up, '+\
    '_9_gold_up, _9_gold_down, '+\
    '_10_BTC_day_up_week_up, _10_BTC_day_down_week_up, '+\
    '_11_BTC_day_up_week_down, _11_BTC_day_down_week_down '+\
    'FROM briefing WHERE lang="'+ language +'"'
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        str_1_world_day_up_week_down = row[0].replace(day_pct, d1_world)
        str_1_world_day_up_week_down = str_1_world_day_up_week_down.replace(week_pct, w1_world)
        str_1_world_day_down_week_up = row[1].replace(day_pct, d1_world)
        str_1_world_day_down_week_up = str_1_world_day_down_week_up.replace(week_pct, w1_world)

        str_2_world_day_up_week_up = row[2].replace(day_pct, d1_world)
        str_2_world_day_up_week_up = str_2_world_day_up_week_up.replace(week_pct, w1_world)
        str_2_world_day_down_week_down = row[3].replace(day_pct, d1_world)
        str_2_world_day_down_week_down = str_2_world_day_down_week_down.replace(week_pct, w1_world)

        str_3_world_day_up_ma10_down = row[4].replace(day_pct, d1_world)
        str_3_world_day_up_ma10_down = str_3_world_day_up_ma10_down.replace(week_pct, w1_world)
        str_3_world_day_down_ma10_up = row[5].replace(day_pct, d1_world)
        str_3_world_day_down_ma10_up = str_3_world_day_down_ma10_up.replace(week_pct, w1_world)

        str_4_world_day_up_ma10_up = row[6].replace(day_pct, d1_world)
        str_4_world_day_up_ma10_up = str_4_world_day_up_ma10_up.replace(week_pct, w1_world)
        str_4_world_day_down_ma10_down = row[7].replace(day_pct, d1_world)
        str_4_world_day_down_ma10_down = str_4_world_day_down_ma10_down.replace(week_pct, w1_world)

        str_5_vix_day_up_week_down = row[8].replace(day_pct, d1_vix)
        str_5_vix_day_up_week_down = str_5_vix_day_up_week_down.replace(week_pct, w1_vix)
        str_5_vix_day_down_week_down = row[9].replace(day_pct, d1_vix)
        str_5_vix_day_down_week_down = str_5_vix_day_down_week_down.replace(week_pct, w1_vix)

        str_6_vix_day_up_week_up = row[10].replace(day_pct, d1_vix)
        str_6_vix_day_up_week_up = str_6_vix_day_up_week_up.replace(week_pct, w1_vix)
        str_6_vix_day_down_week_up = row[11].replace(day_pct, d1_vix)
        str_6_vix_day_down_week_up = str_6_vix_day_down_week_up.replace(week_pct, w1_vix)

        str_7_world_up_jpy_down = row[12].replace(day_pct, d1_jpy)
        str_7_world_up_jpy_down = str_7_world_up_jpy_down.replace(week_pct, w1_jpy)
        str_7_world_down_jpy_down = row[13].replace(day_pct, d1_jpy)
        str_7_world_down_jpy_down = str_7_world_down_jpy_down.replace(week_pct, w1_jpy)

        str_8_world_up_jpy_up = row[14].replace(day_pct, d1_jpy)
        str_8_world_up_jpy_up = str_8_world_up_jpy_up.replace(week_pct, w1_jpy)
        str_8_world_down_jpy_up = row[15].replace(day_pct, d1_jpy)
        str_8_world_down_jpy_up = str_8_world_down_jpy_up.replace(week_pct, w1_jpy)

        str_9_gold_up = row[16].replace(day_pct, d1_gold)
        str_9_gold_up = str_9_gold_up.replace(week_pct, w1_gold)
        str_9_gold_down = row[17].replace(day_pct, d1_gold)
        str_9_gold_down = str_9_gold_down.replace(week_pct, w1_gold)

        str_10_btc_day_up_week_up = row[18].replace(day_pct, d1_btc)
        str_10_btc_day_up_week_up = str_10_btc_day_up_week_up.replace(week_pct, w1_btc)
        str_10_btc_day_down_week_up = row[19].replace(day_pct, d1_btc)
        str_10_btc_day_down_week_up = str_10_btc_day_down_week_up.replace(week_pct, w1_btc)

        str_11_btc_day_up_week_down = row[20].replace(day_pct, d1_btc)
        str_11_btc_day_up_week_down = str_11_btc_day_up_week_down.replace(week_pct, w1_btc)
        str_11_btc_day_down_week_down = row[21].replace(day_pct, d1_btc)
        str_11_btc_day_down_week_down = str_11_btc_day_down_week_down.replace(week_pct, w1_btc)

    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_w1') == 'd1_up_w1_down':
        report = report +' '+ str_1_world_day_up_week_down
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_w1') == 'd1_down_w1_up':
        report = report +' '+ str_1_world_day_down_week_up
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_w1') == 'd1_up_w1_up':
        report = report +' '+ str_2_world_day_up_week_up
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_w1') == 'd1_down_w1_down':
        report = report +' '+ str_2_world_day_down_week_down

    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_ma10') == 'd1_up_ma10_down':
        report = report +' '+ str_3_world_day_up_ma10_down
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_ma10') == 'd1_down_ma10_up':
        report = report +' '+ str_3_world_day_down_ma10_up
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_ma10') == 'd1_up_ma10_up':
        report = report +' '+ str_4_world_day_up_ma10_up
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_ma10') == 'd1_down_ma10_down':
        report = report +' '+ str_4_world_day_down_ma10_down

    if get_condition(symbol_vix, symbol_jpy, 'd1_w1') == 'd1_up_w1_down':
        report = report +' '+ str_5_vix_day_up_week_down
    if get_condition(symbol_vix, symbol_jpy, 'd1_w1') == 'd1_down_w1_down':
        report = report +' '+ str_5_vix_day_down_week_down
    if get_condition(symbol_vix, symbol_jpy, 'd1_w1') == 'd1_up_w1_up':
        report = report +' '+ str_6_vix_day_up_week_up
    if get_condition(symbol_vix, symbol_jpy, 'd1_w1') == 'd1_down_w1_up':
        report = report +' '+ str_6_vix_day_down_week_up

    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_jpy') == 'd1_up_jpy_down':
        report = report +' '+ str_7_world_up_jpy_down
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_jpy') == 'd1_down_jpy_down':
        report = report +' '+ str_7_world_down_jpy_down
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_jpy') == 'd1_up_jpy_up':
        report = report +' '+ str_8_world_up_jpy_up
    if get_condition(symbol_worldstocks, symbol_jpy, 'd1_jpy') == 'd1_down_jpy_up':
        report = report +' '+ str_8_world_down_jpy_up

    if get_condition(symbol_gold, symbol_jpy, 'gold') == 'd1_up':
        report = report +' '+ str_9_gold_up
    if get_condition(symbol_gold, symbol_jpy, 'gold') == 'd1_down':
        report = report +' '+ str_9_gold_down

    if get_condition(symbol_btc, symbol_jpy, 'd1_w1') == 'd1_up_w1_up':
        report = report +' '+ str_10_btc_day_up_week_up
    if get_condition(symbol_btc, symbol_jpy, 'd1_w1') == 'd1_down_w1_up':
        report = report +' '+ str_10_btc_day_down_week_up
    if get_condition(symbol_btc, symbol_jpy, 'd1_w1') == 'd1_up_w1_down':
        report = report +' '+ str_11_btc_day_up_week_down
    if get_condition(symbol_btc, symbol_jpy, 'd1_w1') == 'd1_down_w1_down':
        report = report +' '+ str_11_btc_day_down_week_down

    sql = "SELECT COUNT(*) FROM reports"
    cursor.execute(sql)
    res = cursor.fetchall()
    cnt = 0
    for row in res:
        cnt = row[0]
    if cnt == 0:
        sql = 'INSERT IGNORE INTO reports(lang,market_snapshot) VALUES("'+\
        language +'","'+ report +'")'
    else:
        sql = 'UPDATE reports SET market_snapshot ="'+ report +'" WHERE lang="'+\
        language +'"'

    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

    ret = report
    return ret

def send_intel_report():
    """
    Compose the email for the intelligence report and send mail
    Args:
        None
    Returns:
        None
    """
    num_of_email_limit_per_message = 55
    num_of_second_interval = 60

    l_subject = 'Daily Briefing'
    l_report_url = 'https://app.smartalphatrade.com/intelligence'
    l_msgtext = 'Good day,'+'\n'+ compile_market_snapshot() + '\n'+' '+\
    '\n' +'Access to your intelligence report: '+ l_report_url
    today = datetime.date.today()
    today_str = today.strftime('%Y-%b-%d')
    send_to_email = get_reply_to_email('email')
    send_to_displayname = get_reply_to_email('name')
    subject = today_str + ' - ' + l_subject
    bundle_email(num_of_email_limit_per_message, num_of_second_interval,
                 send_to_email, send_to_displayname, subject, l_msgtext)


def bundle_email(num_of_email_in_group, num_of_second_interval,
                 to_email, to_display_name, subject, textmsg):
    """
    Create the mailing list
    Args:
        Integer: Number of email max to group in a single mail to avoid
                    limitation from the internet service provider
        Integer: Number of seconds interval between mail send to avoid
                    limitation from the internet service provider
        String: Email address used as a sender
        String: Display name used for the sender
        String: Subject of the email
        String: Text of the email
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
    sql = 'SELECT DISTINCT username FROM users JOIN instruments ON '+\
    'instruments.owner = users.id '+\
    'WHERE users.is_bot=0 AND users.deactivated=0 AND '+\
    '(email_subscription="ALL" OR email_subscription="DIR") '
    cursor.execute(sql)
    res = cursor.fetchall()

    i = 1
    bcc = []

    for row in res:
        email = row[0]

        if i <= num_of_email_in_group:
            bcc.append(email)
            i += 1
        else:
            send_mail(to_email, to_display_name, bcc, subject, textmsg)
            debug('waiting for '+ str(num_of_second_interval) + ' seconds before the next batch...')
            time.sleep(num_of_second_interval)
            bcc.clear()
            bcc.append(email)
            i = 1

    send_mail(to_email, to_display_name, bcc, subject, textmsg)

    cursor.close()
    connection.close()
