# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import datetime
import time
from pathlib import Path
import smtplib

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

'''
--------------------------------------------------------------------------------
Instruction:
to email: get_reply_to_email('email')
to to_displayName: get_reply_to_email('name')
textmsg: use backslash n to go to next line.
--------------------------------------------------------------------------------
'''
def send_mail(to_email,to_displayName,bcc,subject,textmsg):
    r = ''
    try:
        tolist = [to_email] + bcc
        smtp_user = access_obj.smtp_username()
        smtp_pwd = access_obj.smtp_password()
        smtpserver = smtplib.SMTP( access_obj.smtp_server(),access_obj.smtp_port() )

        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo() # extra characters to permit edit
        smtpserver.login(smtp_user, smtp_pwd)
        header = 'To:' + to_email + '\n' + 'From: '+ to_displayName +' <' + to_email + '>\n' +\
                 'Subject:'+ subject +' \n'

        print(header)
        seperator = ', '
        print(seperator.join(bcc))

        msg = header + '\n' + textmsg + '\n' + get_email_txt_signature() + '\n'

        smtpserver.sendmail(smtp_user, tolist, msg)
        smtpserver.quit()

        r = to_email + ' - ' + bcc + ' - Sending email...'

    except Exception as e: print(e)
    return r

def process_mail_queue():
    try:
        import pymysql.cursors
        connection = pymysql.connect(host=db_srv,
                                     user=db_usr,
                                     password=db_pwd,
                                     db=db_name,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'SELECT id, from_email, from_email_displayname, send_to_email_bcc, email_subject, email_content FROM email_queue ORDER BY id'
        cr.execute(sql)
        rs = cr.fetchall()

        rm_query = ''

        id = 0
        from_email_displayname = ''
        email_subject = ''
        email_content = ''

        i = 1
        condition = ''
        where = ''

        for row in rs:
            from_email = []
            send_to_email_bcc = []
            id = row[0]
            from_email.append(row[1])
            from_email_displayname = row[2]
            send_to_email_bcc.append(row[3])
            email_subject = row[4]
            email_content = row[5]
            print( send_mail(from_email,from_email_displayname,send_to_email_bcc,email_subject,email_content) )
            if i > 1: condition = ' OR '
            where = where + condition + ' id='+ str(id)
            i += 1
        try:
            rm_query = 'DELETE FROM email_queue WHERE ' + where
            print(rm_query)
            cr.execute(rm_query)
            connection.commit()
        except:
            print('No email in queue')
            pass

        cr.close()
        connection.close()

    except Exception as e: print(e)
