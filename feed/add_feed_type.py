""" Import feed type into the database """
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


def add_feed_type(feed_id, feed_type):
    """
    Import brokers and affiliate link to the database.
    Args:
        Integer: id for the feed.
        String: short name or description for the type of feed.
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
    sql = "INSERT IGNORE INTO feed_type(id, feed_type) VALUES ('"+str(feed_id)+"','"+feed_type+"')"
    cursor.execute(sql)
    connection.commit()
    debug(sql +": "+ os.path.basename(__file__))
    cursor.close()
    connection.close()

def set_feed_function(func_name, sub_func, what):
    """
    Return the function html formatting as per func_name
    Args:
        String: Label, name of function
        String: Instrument symbol or sub function
        String: label = display label. value = for use in the column.
    Returns:
        String: html for function label
    """
    ret = ''
    if what == 'label':
        function_label = '<span class="btn btn-outline-info">'+ str(func_name) +' </span>'
        if sub_func != '':
            sub_func_label = '<span class="btn btn-outline-info">'+ str(sub_func) +' </span>'
        else:
            sub_func_label = ''
        ret = sub_func_label + '&nbsp;' + function_label + '&nbsp;&nbsp;'
    else:
        ret = sub_func + ' ' + func_name
        
    return ret
