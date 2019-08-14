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

'''
--------------------------------------------------------------------------------
Instruction:
to email: get_reply_to_email('email')
to to_displayName: get_reply_to_email('name')
textmsg: use backslash n to go to next line.
--------------------------------------------------------------------------------
'''
def send_mail(to_email,to_displayName,bcc,subject,textmsg):
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

    except Exception as e: print(e)
