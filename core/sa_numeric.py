# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os
from pathlib import Path
import numpy as np
import math as math
from math import exp, expm1


pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username(); db_pwd = access_obj.password(); db_name = access_obj.db_name(); db_srv = access_obj.db_server()

import pymysql.cursors

def get_pct_change(ini_val,new_val):

    if not new_val == 0:
        if new_val < ini_val:
            r =  ( (ini_val - new_val) / ini_val ) * (-1)
        else:
            r = (new_val - ini_val) / new_val
    else:
        r = 0

    return r


def get_stdev(sql):

    r = 0
    try:
        #sql with just one numerical value to compute standard deviation
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        print(sql)
        cr.execute(sql)
        a = list( cr.fetchall() )
        r = np.std(a)
        print('stdev='+str(r) )
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r

def get_volatility_risk(sql,is_portf,s):

    r = 0

    try:
        #sql with one numerical column to compute volatility risk
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)

        if is_portf:
            sql_i = "SELECT account_reference FROM instruments WHERE symbol='"+ s +"'"
            cr.execute(sql_i)
            rs = cr.fetchall()
            for row in rs: lp = row[0]
        else:
            cr.execute(sql)
            rs = cr.fetchall()
            for row in rs: lp = row[0]

        stdev = get_stdev(sql)
        rp = lp - stdev
        r = abs( get_pct_change(lp,rp)  )
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r


def get_mdd(sql):

    r = 0
    try:
        #sql with just one numerical value to compute maximum drawdown
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        cr.execute(sql)
        rs = cr.fetchall()
        top = 0
        breset = math.pow(10,100)
        bottom = breset
        pct_dd = 0
        cur_dd = 0
        for row in rs:
            val = row[0]

            if val > top:
                top = val
                bottom = breset

            if val < bottom:
                bottom = val

            if bottom < top:
                cur_dd = abs( get_pct_change(bottom,top) )
            else:
                cur_dd = 0

            if cur_dd > pct_dd:
                pct_dd = cur_dd

        r = pct_dd
        print('mdd='+ str(r) )
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r

def get_romad(sql):

    r = 0
    try:
        #sql with one column as numerical value to compute return on maximum drawdown
        #ordered by date ASC
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd,db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        cr.execute(sql)
        rs = cr.fetchall()
        i = 0
        first = 0
        last = 0
        for row in rs:
            if i == 0:
                first = row[0]
            last = row[0]
            i += 1

        print('f='+str(first) + ' l='+str(last) )

        rt = get_pct_change(first,last)
        dd = get_mdd(sql)

        r = rt / dd
        print('romad='+ str(r) )
        cr.close()
        connection.close()
    except Exception as e: print(e)

    return r
