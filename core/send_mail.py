""" Send email functions """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import smtplib
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug, get_email_txt_signature, get_reply_to_email
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

'''
--------------------------------------------------------------------------------
Instruction:
to email: get_reply_to_email('email')
to to_displayName: get_reply_to_email('name')
textmsg: use backslash n to go to next line.
--------------------------------------------------------------------------------
'''
def send_mail(to_email, to_display_name, bcc, subject, textmsg):
    """
    Send email
    Args:
        String: Sender used in the email
        String: Display name of the sender used in the email
        String: BCC which is email(s) to be send to...
        String: email subject
        String: email text content
    Returns:
        String: Related information.
    """
    ret = ''
    tolist = [to_email] + bcc
    smtp_user = ACCESS_OBJ.smtp_username()
    smtp_pwd = ACCESS_OBJ.smtp_password()
    smtpserver = smtplib.SMTP(ACCESS_OBJ.smtp_server(), ACCESS_OBJ.smtp_port())

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo() # extra characters to permit edit
    smtpserver.login(smtp_user, smtp_pwd)
    header = 'To:' + to_email + '\n' + 'From: '+ to_display_name +' <' + to_email + '>\n' +\
             'Subject:'+ subject +' \n'

    debug(header)
    seperator = ', '
    debug(seperator.join(bcc))

    msg = header + '\n' + textmsg + '\n' + get_email_txt_signature() + '\n'

    smtpserver.sendmail(smtp_user, tolist, msg)
    smtpserver.quit()
    return ret

def process_mail_queue():
    """
    Process email in the table email_queue.
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
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'SELECT id, from_email, from_email_displayname, send_to_email_bcc, '+\
    'email_subject, email_content FROM email_queue ORDER BY priority, id'
    cursor.execute(sql)
    res = cursor.fetchall()

    rm_query = ''

    email_id = 0
    from_email_displayname = ''
    email_subject = ''
    email_content = ''

    i = 1
    condition = ''
    where = ''

    for row in res:
        send_to_email_bcc = []
        email_id = row[0]
        from_email = row[1]
        from_email_displayname = row[2]
        send_to_email_bcc.append(row[3])
        email_subject = row[4]
        email_content = row[5]

        if from_email == '' or from_email is None:
            from_email = get_reply_to_email('email')
            from_email_displayname = get_reply_to_email('name')
        if send_to_email_bcc[0] == '':
            send_to_email_bcc.append(get_reply_to_email('tech'))

        debug(send_mail(from_email, from_email_displayname, send_to_email_bcc,
                        email_subject, email_content))
        if i > 1:
            condition = ' OR '
        where = where + condition + ' id='+ str(email_id)
        i += 1

    rm_query = 'DELETE FROM email_queue WHERE ' + where
    debug(rm_query)
    cursor.execute(rm_query)
    connection.commit()

    cursor.close()
    connection.close()
