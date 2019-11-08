# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

from pathlib import Path

import pymysql.cursors

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


cr = connection.cursor(pymysql.cursors.SSCursor)
sql = "DELETE FROM email_templates"
cr.execute(sql)
connection.commit()


######## English ########
lang_en = "en"
new_user_welcome_subject_en = "{fullname}, welcome to SmartAlpha"
new_user_welcome_content_en = "{fullname},\n Thank you for joining SmartAlpha.\n "+\
"Your login is your email {email}. We are happy to welcome you as a member of our growing community.\n "+\
" Feel free to get in touch with us. We are here to support you and to listen."

sql = "INSERT IGNORE INTO email_templates(lang, new_user_welcome_subject, new_user_welcome_content) VALUES "+\
"('"+lang_en+"', '"+  new_user_welcome_subject_en +"', '"+ new_user_welcome_content_en +"' " + ")"
debug(sql)

try:
    cr.execute(sql)
    connection.commit()
except Exception as e: debug(e)

cr.close()
connection.close()
