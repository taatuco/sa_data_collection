# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
from pathlib import Path
from send_mail import *

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

def get_condition(s,sj,w):
    r = ''
    w1 = 0
    d1 = 0
    ma10 = 0
    jpyd1 = 0
    try:

        import pymysql.cursors
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT w1, d1, unit FROM instruments WHERE symbol = "'+ str(s) +'" '
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: w1 = row[0]; d1 = row[1]

        sql = 'SELECT w1, d1 FROM instruments WHERE symbol = "'+ str(sj) +'" '
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: w1 = row[0]; jpyd1 = row[1]


        sql = 'SELECT ma10 FROM price_instruments_data WHERE symbol = "'+ str(s) +'" ORDER BY date DESC LIMIT 1'
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: ma10 = row[0]

        cr.close()

        if w == 'd1_w1':
            if d1 > 0 and w1 < 0: r = 'd1_up_w1_up'
            if d1 < 0 and w1 > 0: r = 'd1_down_w1_up'
            if d1 > 0 and w1 > 0: r = 'd1_up_w1_up'
            if d1 < 0 and w1 < 0: r = 'd1_down_w1_down'
        if w == 'd1_ma10':
            if d1 > 0 and d1 < ma10: r = 'd1_up_ma10_down'
            if d1 < 0 and d1 > ma10: r = 'd1_down_ma10_up'
            if d1 > 0 and d1 > ma10: r = 'd1_up_ma10_up'
            if d1 < 0 and d1 < ma10: r = 'd1_down_ma10_down'
        if w == 'd1_jpy':
            if d1 > 0 and jpyd1 < 0: r = 'd1_up_jpy_down'
            if d1 < 0 and jpyd1 < 0: r = 'd1_down_jpy_down'
            if d1 > 0 and jpyd1 > 0: r = 'd1_up_jpy_up'
            if d1 < 0 and jpyd1 > 0: r = 'd1_down_jpy_up'
        if w == 'gold':
            if d1 > 0: r = 'd1_up'
            if d1 < 0: r = 'd1_down'


    except Exception as e: print(e)
    return r

def get_perf(s,p):
    r = ''
    w1 = ''
    d1 = ''
    unit = ''
    try:
        import pymysql.cursors
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT w1, d1, unit FROM instruments WHERE symbol = "'+ str(s) +'" '
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            w1 = str(row[0])
            d1 = str(row[1])
            unit = str(row[2])

        sep = ''
        if unit !='%': sep = ' '
        if p == 'd1': r = d1 + ' ' + unit
        if p == 'w1': r = w1 + ' ' + unit

    except Exception as e: print(e)
    return r

def compile_market_snapshot():
    r = ''
    report = ''
    try:
        language = 'en'
        symbol_worldstocks = 'NYSEARCA:URTH'; d1_worldstocks = get_perf(symbol_worldstocks,'d1'); w1_worldstocks = get_perf(symbol_worldstocks,'w1')
        symbol_vix = 'INDEXCBOE:BVZ'; d1_vix = get_perf(symbol_vix,'d1'); w1_vix = get_perf(symbol_vix,'w1')
        symbol_jpy = 'USDJPY'; d1_jpy = get_perf(symbol_jpy,'d1'); w1_jpy = get_perf(symbol_jpy,'w1')
        symbol_gold = 'GLD'; d1_gold = get_perf(symbol_gold,'d1'); w1_gold = get_perf(symbol_gold,'w1')
        symbol_btc = 'BITCOIN'; d1_btc = get_perf(symbol_btc,'d1'); w1_btc = get_perf(symbol_btc,'w1')

        day_percent = '{day_percent}'
        week_percent = '{week_percent}'

        import pymysql.cursors
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
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
        cr.execute(sql)
        rs = cr.fetchall()

        for row in rs:
            _1_worldstocks_day_up_week_down = ( row[0].replace(day_percent,d1_worldstocks) ).replace(week_percent,w1_worldstocks)
            _1_worldstocks_day_down_week_up = ( row[1].replace(day_percent,d1_worldstocks) ).replace(day_percent,w1_worldstocks)
            _2_worldstocks_day_up_week_up = ( row[2].replace(day_percent,d1_worldstocks) ).replace(day_percent,w1_worldstocks)
            _2_worldstocks_day_down_week_down = ( row[3].replace(day_percent,d1_worldstocks) ).replace(day_percent,w1_worldstocks)

            _3_worldstocks_day_up_ma10_down = ( row[4].replace(day_percent,d1_worldstocks) ).replace(day_percent,w1_worldstocks)
            _3_worldstocks_day_down_ma10_up = ( row[5].replace(day_percent,d1_worldstocks) ).replace(day_percent,w1_worldstocks)
            _4_worldstocks_day_up_ma10_up = ( row[6].replace(day_percent,d1_worldstocks) ).replace(day_percent,w1_worldstocks)
            _4_worldstocks_day_down_ma10_down = ( row[7].replace(day_percent,d1_worldstocks) ).replace(day_percent,w1_worldstocks)

            _5_vix_day_up_week_down = ( row[8].replace(day_percent,d1_vix) ).replace(day_percent,w1_vix)
            _5_vix_day_down_week_down = ( row[9].replace(day_percent,d1_vix) ).replace(day_percent,w1_vix)
            _6_vix_day_up_week_up = ( row[10].replace(day_percent,d1_vix) ).replace(day_percent,w1_vix)
            _6_vix_day_down_week_up = ( row[11].replace(day_percent,d1_vix) ).replace(day_percent,w1_vix)

            _7_worldstocks_up_JPY_down = ( row[12].replace(day_percent,d1_jpy) ).replace(day_percent,w1_jpy)
            _7_worldstocks_down_JPY_down = ( row[13].replace(day_percent,d1_jpy) ).replace(day_percent,w1_jpy)
            _8_workdstocks_up_JPY_up = ( row[14].replace(day_percent,d1_jpy) ).replace(day_percent,w1_jpy)
            _8_worldstocks_down_JPY_up = ( row[15].replace(day_percent,d1_jpy) ).replace(day_percent,w1_jpy)

            _9_gold_up = ( row[16].replace(day_percent,d1_gold) ).replace(day_percent,w1_gold)
            _9_gold_down = ( row[17].replace(day_percent,d1_gold) ).replace(day_percent,w1_gold)

            _10_BTC_day_up_week_up = ( row[18].replace(day_percent,d1_btc) ).replace(day_percent,w1_btc)
            _10_BTC_day_down_week_up = ( row[19].replace(day_percent,d1_btc) ).replace(day_percent,w1_btc)
            _11_BTC_day_up_week_down = ( row[20].replace(day_percent,d1_btc) ).replace(day_percent,w1_btc)
            _11_BTC_day_down_week_down = ( row[21].replace(day_percent,d1_btc) ).replace(day_percent,w1_btc)

        if get_condition(symbol_worldstocks,symbol_jpy,'d1_w1') == 'd1_up_w1_down': report = report +' '+ _1_worldstocks_day_up_week_down
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_w1') == 'd1_down_w1_up': report = report +' '+ _1_worldstocks_day_down_week_up
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_w1') == 'd1_up_w1_up': report = report +' '+ _2_worldstocks_day_up_week_up
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_w1') == 'd1_down_w1_down': report = report +' '+ _2_worldstocks_day_down_week_down

        if get_condition(symbol_worldstocks,symbol_jpy,'d1_ma10') == 'd1_up_ma10_down': report = report +' '+ _3_worldstocks_day_up_ma10_down
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_ma10') == 'd1_down_ma10_up': report = report +' '+ _3_worldstocks_day_down_ma10_up
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_ma10') == 'd1_up_ma10_up': report = report +' '+ _4_worldstocks_day_up_ma10_up
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_ma10') == 'd1_down_ma10_down': report = report +' '+ _4_worldstocks_day_down_ma10_down

        if get_condition(symbol_vix,symbol_jpy,'d1_w1') == 'd1_up_w1_down': report = report +' '+ _5_vix_day_up_week_down
        if get_condition(symbol_vix,symbol_jpy,'d1_w1') == 'd1_down_w1_down': report = report +' '+ _5_vix_day_down_week_down
        if get_condition(symbol_vix,symbol_jpy,'d1_w1') == 'd1_up_w1_up': report = report +' '+ _6_vix_day_up_week_up
        if get_condition(symbol_vix,symbol_jpy,'d1_w1') == 'd1_down_w1_up': report = report +' '+ _6_vix_day_down_week_up

        if get_condition(symbol_worldstocks,symbol_jpy,'d1_jpy') == 'd1_up_jpy_down': report = report +' '+ _7_worldstocks_up_JPY_down
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_jpy') == 'd1_down_jpy_down': report = report +' '+ _7_worldstocks_down_JPY_down
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_jpy') == 'd1_up_jpy_up': report = report +' '+ _8_workdstocks_up_JPY_up
        if get_condition(symbol_worldstocks,symbol_jpy,'d1_jpy') == 'd1_down_jpy_up': report = report +' '+ _8_worldstocks_down_JPY_up

        if get_condition(symbol_gold,symbol_jpy,'gold') == 'd1_up': report = report +' '+ _9_gold_up
        if get_condition(symbol_gold,symbol_jpy,'gold') == 'd1_down': report = report +' '+ _9_gold_down

        if get_condition(symbol_btc,symbol_jpy,'d1_w1') == 'd1_up_w1_up': report = report +' '+ _10_BTC_day_up_week_up
        if get_condition(symbol_btc,symbol_jpy,'d1_w1') == 'd1_down_w1_up': report = report +' '+ _10_BTC_day_down_week_up
        if get_condition(symbol_btc,symbol_jpy,'d1_w1') == 'd1_up_w1_down': report = report +' '+ _11_BTC_day_up_week_down
        if get_condition(symbol_btc,symbol_jpy,'d1_w1') == 'd1_down_w1_down': report = report +' '+ _11_BTC_day_down_week_down

        sql = "SELECT COUNT(*) FROM reports"
        cr.execute(sql)
        rs = cr.fetchall()
        cnt = 0
        for row in rs: cnt = row[0]
        if cnt == 0:
            sql = 'INSERT IGNORE INTO reports(lang,market_snapshot) VALUES("'+ language +'","'+ report +'")'
        else:
            sql = 'UPDATE reports SET market_snapshot =""'+ report +'" WHERE lang="'+ language +'"'

        cr.execute(sql)
        connection.commit()
        cr.close()

        r = report

    except Exception as e: print(e)
    return r

def send_intel_report():
    try:
        num_of_email_limit_per_message = 55
        num_of_second_interval = 60

        l_subject = 'Daily Briefing'
        l_report_url = 'http://smartalphatrade.com/intelligence'
        l_msgtext = 'Hello,'+'\n'+ compile_market_snapshot() + '\n'+'We have compiled your intelligence briefing for today. '+ '\n' +'Access to your report: '+ l_report_url
        today = datetime.date.today()
        todayStr = today.strftime('%Y-%b-%d')
        send_to_email = get_reply_to_email('email')
        send_to_displayname = get_reply_to_email('name')
        subject = todayStr + ' - ' + l_subject

        bundle_email(num_of_email_limit_per_message, num_of_second_interval, send_to_email, send_to_displayname, subject, l_msgtext)

    except Exception as e: print(e)


def bundle_email(num_of_email_in_group, num_of_second_interval, to_email, to_displayName, subject, textmsg):
    try:

        import pymysql.cursors
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT DISTINCT username FROM users JOIN instruments ON instruments.owner = users.id WHERE users.is_bot=0 AND users.deactivated=0'
        cr.execute(sql)
        rs = cr.fetchall()

        i = 1
        bcc = []

        for row in rs:
            email = row[0]

            if i <= num_of_email_in_group:
                bcc.append(email)
                i += 1
            else:
                send_mail(to_email,to_displayName,bcc,subject,textmsg)
                print('waiting for '+ str(num_of_second_interval) + ' seconds before the next batch...' )
                time.sleep(num_of_second_interval)
                bcc.clear()
                bcc.apeend(email)
                i = 1

        send_mail(to_email,to_displayName,bcc,subject,textmsg)

        cr.close()
        connection.close()

    except Exception as e: print(e)
