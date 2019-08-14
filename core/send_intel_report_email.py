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

def send_intel_report():
    try:
        num_of_email_limit_per_message = 55
        num_of_second_interval = 60

        l_subject = 'Intelligence Report'
        l_report_url = 'http://smartalphatrade.com/?dashboard=1'
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
        sql = 'SELECT DISTINCT username FROM users JOIN instruments ON instruments.owner = users.id WHERE users.is_bot=0'
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
