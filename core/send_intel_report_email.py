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

def compile_market_snapshot():
    try:
        language = 'en'

        symbol_worldstocks = 'NYSEARCA:URTH'; d1_worldstocks = 0; w1_wordstocks = 0; unit_worldstocks = '%'
        symbol_vix = 'INDEXCBOE:BVZ'; d1_vix = 0; w1_vix = 0; unit_vix = '%'
        symbol_jpy = 'USDJPY'; d1_jpy = 0; w1_jpy = 0; unit_jpy = '%'
        symbol_gold = 'GLD'; d1_gld = 0; w1_gld = 0; unit_gold = '%'
        symbol_btc = 'BITCOIN'; d1_btc = 0; w1_btc = 0; unit_btc = '%'

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
        'lang, '+\
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
            _1_worldstocks_day_up_week_down = row[0]
            _1_worldstocks_day_down_week_up = row[1]
            _2_worldstocks_day_up_week_up = row[2]
            _2_worldstocks_day_down_week_down = row[3]
            _3_worldstocks_day_up_ma10_down = row[4]
            _3_worldstocks_day_down_ma10_up = row[5]
            _4_worldstocks_day_up_ma10_up = row[6]
            _4_worldstocks_day_down_ma10_down = row[7]
            _5_vix_day_up_week_down = row[8]
            _5_vix_day_down_week_down = row[9]
            _6_vix_day_up_week_up = row[10]
            _6_vix_day_down_week_up = row[11]
            _7_worldstocks_up_JPY_down = row[12]
            _7_worldstocks_down_JPY_down = row[13]
            _8_workdstocks_up_JPY_up = row[14]
            _8_worldstocks_down_JPY_up = row[15]
            _9_gold_up = row[16]
            _9_gold_down = row[17]
            _10_BTC_day_up_week_up = row[18]
            _10_BTC_day_down_week_up = row[19]
            _11_BTC_day_up_week_down = row[20]
            _11_BTC_day_down_week_down = row[21]


    except Exception as e: print(e)

def send_intel_report():
    try:
        num_of_email_limit_per_message = 55
        num_of_second_interval = 60

        l_subject = 'Daily Briefing'
        l_report_url = 'http://smartalphatrade.com/intelligence'
        l_msgtext = 'Hello,'+'\n'+'We have compiled your intelligence briefing for today. '+ '\n' +'Access to your report: '+ l_report_url
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
