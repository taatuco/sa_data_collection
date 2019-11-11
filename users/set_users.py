""" Functionalities related to users """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
import datetime
import random
import string
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def set_user_uid():
    """
    Set user uid with a generated random string
    Args:
        None
    Returns:
        String: a random string
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=99))

def set_user_avatar_id():
    """
    Select randomly an avatar
    Args:
        None
    Returns:
        Int: a random integer from 1 to av_max
    """
    av_max = 19
    return random.randint(1, av_max)

def set_nickname():
    """
    Create a nickname from a random selection of words
    Args:
        None
    Returns:
        String: a random nickname
    """
    p_1 = ''
    p_2 = ''
    num = ''
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT part_one FROM randwords ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        p_1 = row[0]
    sql = "SELECT part_two FROM randwords ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        p_2 = row[0]
    cursor.close()
    connection.close()
    num = str(random.randint(1, 99))
    ret = p_1 + p_2 + num
    return ret

def set_default_profile():
    """
    Set the default trader's profile from a random selection
    Args:
        None
    Returns:
        String: a random default trader's profile
    """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT asset_class_id as p FROM asset_class UNION "+\
    "SELECT market_id as p FROM markets ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    cursor.close()
    connection.close()
    ret = ret.replace('PF:', '')
    ret = ret.replace('BD:', '')
    return ret

def gen_users(number_of_users):
    """
    Generate X number of template users for the create of example
    of strategy portfolios.
    Args:
        Int: number of users to create.
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
    date_today = datetime.datetime.now()
    date_today = date_today.strftime('%Y%m%d')
    for i in range(number_of_users):
        if i == 0:
            default_user = 'smartalpha'
            uid = set_user_uid()
            name = default_user
            nickname = name
            username = name + '@smartalphatrade.com'
            password = set_user_uid()
            avatar_id = set_user_avatar_id()
            created_on = str(date_today)
            default_profile = ''
            lang = 'en'
            is_bot = 1
        else:
            uid = set_user_uid()
            name = set_nickname()
            nickname = name
            username = name + '@smartalphatrade.com'
            password = set_user_uid()
            avatar_id = set_user_avatar_id()
            created_on = str(date_today)
            default_profile = set_default_profile()
            lang = 'en'
            is_bot = 1

        sql = "INSERT IGNORE INTO users"+\
        "(uid, name, nickname, username, password, avatar_id, created_on, "+\
        "default_profile, lang, is_bot) VALUES "+\
        "('"+ str(uid) +"','"+ str(name) +"','"+ str(nickname) +\
        "','"+ str(username) +"','"+ str(password) +"',"+ str(avatar_id) +\
        ",'"+ str(created_on) +"','"+ str(default_profile) +"','"+ str(lang) +\
        "',"+str(is_bot)+")"
        debug(sql)
        cursor.execute(sql)
        connection.commit()
    cursor.close()
    connection.close()

gen_users(1000)
