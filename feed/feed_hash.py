""" xxx """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import pymysql.cursors

PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, get_hash_string
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def hash_feed(what, feed_type):
    """
    what = 'news'
    what = 'url'
    """
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT short_title, url FROM feed WHERE hash = '' AND type= "+ str(feed_type) + " LOCK IN SHARE MODE"
    cursor.execute(sql)
    res = cursor.fetchall()
    short_title = ''
    url = ''
    hash_this = ''
    column = ''
    for row in res:
        short_title = row[0]
        url = row[1]

        if what == 'news':
            hash_this = short_title
            column = 'short_title'
        else:
            hash_this = url
            column = 'url'

        cr_u = connection.cursor(pymysql.cursors.SSCursor)
        sql_u = "UPDATE feed SET "+\
        "hash = '"+ get_hash_string(str(hash_this)) +"' "+\
        "WHERE "+ column +" = '"+ str(hash_this) +"'" + ' AND type = ' + str(feed_type)
        cr_u.execute(sql_u)
        connection.commit()

    cursor.close()
    connection.close()
