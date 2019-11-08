""" Import email templates into the database """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import debug, SmartAlphaPath
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()


def set_email_templates():
    """
    Import email text template into the database.
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
    sql = "DELETE FROM email_templates"
    cursor.execute(sql)
    connection.commit()

    ######## English ########
    lang_en = "en"
    new_user_welcome_subject_en = "{fullname}, welcome to SmartAlpha"
    new_user_welcome_content_en = "{fullname},\n Thank you for joining SmartAlpha.\n "+\
    "Your login is your email {email}. We are happy to welcome "+\
    "you as a member of our growing community.\n "+\
    " Feel free to get in touch with us. We are here to support you and to listen."

    sql = "INSERT IGNORE INTO email_templates"+\
    "(lang, new_user_welcome_subject, new_user_welcome_content) VALUES "+\
    "('"+lang_en+"', '"+  new_user_welcome_subject_en +"', '"+\
    new_user_welcome_content_en +"' " + ")"
    debug(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

set_email_templates()
