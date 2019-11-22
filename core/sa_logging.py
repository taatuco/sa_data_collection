""" Log in table log status for each running module """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
from datetime import timedelta
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def log_this(module, status):
    """
    Insert in log table running module and status.
    status 0 is starting of the module, and status 1 is terminated.
    Args:
        String: Module Name
        Integer: Status of the module 1 or 0.
    Returns:
        None
    """
    if module != '':
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = 'INSERT IGNORE INTO log(module, status) VALUES ("'+\
        str(module) +'",'+\
        str(status) +')'
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()

        clear_log()


def clear_log():
    """
    Clear log entries which are older than 10 days
    Args:
        None
    Returns:
        None
    """
    date_reset = datetime.datetime.now() - timedelta(days=10)
    date_reset = date_reset.strftime("%Y%m%d")
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = 'DELETE FROM log WHERE date_time < ' + str(date_reset)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

def update_data_is_terminated():
    """
    Inform about if update data is all done by checking
    in the log table.
    Args:
        None
    Returns:
        Boolean: Return True if terminated
    """
    log_caption = 'Data update terminated'
    date_today = datetime.datetime.now()
    date_today = date_today.strftime("%Y%m%d")
    ret = False

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT COUNT(*) FROM log "+\
    "WHERE date_time >= "+ str(date_today) +\
    " AND module='"+ str(log_caption) +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    count_log = 0
    for row in res:
        count_log = row[0]

    if count_log != 0:
        ret = True

    return ret

def log_update_data_terminated():
    """
    Log in the log table in database as update data is done.
    Args:
        None
    Returns:
        None
    """
    log_caption = 'Data update terminated'
    log_this(log_caption, 1)
