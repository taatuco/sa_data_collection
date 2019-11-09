""" Generate strategy portfolio """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import random
import pymysql.cursors
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath, get_portf_suffix, debug
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_pwd()))
from sa_access import sa_db_access
ACCESS_OBJ = sa_db_access()
DB_USR = ACCESS_OBJ.username()
DB_PWD = ACCESS_OBJ.password()
DB_NAME = ACCESS_OBJ.db_name()
DB_SRV = ACCESS_OBJ.db_server()

def set_portf_symbol():
    """
    Set and generate a portfolio symbol from randomwords.
    Args:
        None
    Returns:
        String: A Random symbol for strategy porfolio.
    """
    ret = ''
    symbol = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT part_three FROM randwords ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    rs = cursor.fetchall()
    for row in rs: symbol = symbol + row[0]
    symbol = symbol + str( random.randint(1,999) )
    ret = get_portf_suffix() + symbol.upper()
    cursor.close()
    connection.close()
    return ret

def set_portf_fullname(symbol,asset_class,market,strategy_type):
    """
    Set and generate strategy portfolio fullname
    Args:
        String: Symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    ret = ''
    fullname = symbol.replace(get_portf_suffix(),'')
    ret = fullname + ' ' + market + ' ' + asset_class + ' ' + strategy_type
    return ret

def get_nickname(id):
    """
    Get user's nickname from id.
    Args:
        Int: id of the user
    Returns:
        String: User's nickname
    """    
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT nickname FROM users WHERE id="+ str(id)
    cursor.execute(sql)
    rs = cursor.fetchall()
    for row in rs:
        ret = row[0]
    cursor.close()
    connection.close()
    return ret

def get_portf_description(asset_class,market,strategy_type,uid):
    """
    Generate and get strategy portfolio description
    Args:
        String: Asset class
        String: Market
        String: Strategy type (Long, Short...)
    Returns:
        String: A text that describe the strategy portfolio.
    """    
    ret = ''
    try:
        connection = pymysql.connect(host=DB_SRV,
                                     user=DB_USR,
                                     password=DB_PWD,
                                     db=DB_NAME,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT portf_description FROM labels WHERE lang = '"+ "en" +"'"
        cursor.execute(sql)
        rs = cursor.fetchall()
        for row in rs: portf_description = row[0]
        nickname = get_nickname(uid)
        market_asset_class = asset_class + ' ' + market + ' '+ strategy_type
        portf_description = portf_description.replace('{market_asset_class}',market_asset_class)
        portf_description = portf_description.replace('{nickname}',nickname)
        ret = portf_description
        cursor.close()
        connection.close()
    except Exception as e: debug(e)
    return ret

def get_strategy():
    """
    Get a strategy type for the generated strategy portfolio.
    A strategy type randomly selected from available strategy type.
    Args:
        None
    Returns:
        String: A strategy type randomly selected.
    """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT codename FROM strategies ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    rs = cursor.fetchall()
    for row in rs:
        ret = row[0]
    return ret

def get_asset_class_name(asset_class_id):
    """
    Get the asset class name from the asset class id
    Args:
        String: Asset class id
    Returns:
        String: the asset class name.
    """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT asset_class_name FROM asset_class WHERE asset_class_id='"+ str(asset_class_id) +"' "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    return ret

def get_market_name(market_id):
    """
    Get the market name from its id
    Args:
        String: Market id
    Returns:
        String: Market name.
    """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT market_label FROM markets WHERE market_id='"+ str(market_id) +"' "
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        ret = row[0]
    return ret

def get_decimal_places(asset_class_id):
    """
    Get decimal places used by the selected asset_class.
    Return the largest used decimal places of the asset class as per arg.
    Args:
        String: Asset Class
    Returns:
        Int: Decimal places
    """
    ret = 2
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT decimal_places FROM instruments WHERE asset_class = '"+ str(asset_class_id) +"' ORDER BY decimal_places DESC LIMIT 1"
    cr.execute(sql)
    rs = cr.fetchall()
    for row in rs:
        ret = row[0]
    return ret

def get_unit(m):
    """
    Set and generate strategy portfolio fullname
    Args:
        String: Symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT currency_code FROM markets WHERE market_id = '"+ str(m) +"' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: debug(e)
    return r

def set_portf_owner():
    """
    Set and generate strategy portfolio fullname
    Args:
        String: Symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT id FROM users WHERE is_bot=1 ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: debug(e)
    return r

def select_allocation(ac,m):
    """
    Set and generate strategy portfolio fullname
    Args:
        String: Symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    r = ''
    try:
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT symbol FROM instruments WHERE symbol NOT LIKE '%"+ get_portf_suffix() +"%' AND asset_class = '"+ str(ac) +"' AND market = '"+ str(m) +"' ORDER BY RAND() LIMIT 1"
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs: r = row[0]
    except Exception as e: debug(e)
    return r

def gen_portf_allocation(s,ac,m,sy):
    """
    Set and generate strategy portfolio fullname
    Args:
        String: Symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    try:
        strategy_order_type = 'long/short'
        if sy == 'l': strategy_order_type = 'long'
        if sy == 's': strategy_order_type = 'short'
        strategy_conviction = 'neutral'

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)

        sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, strategy_order_type, strategy_conviction) VALUES "+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
        "('"+ str(s) +"','"+ select_allocation(ac,m) +"',1,'"+ strategy_order_type +"','"+ strategy_conviction +"')"
        debug(sql)
        cr.execute(sql)
        connection.commit()
        cr.close()
        connection.close()
    except Exception as e: debug(e)

def create_portf(ac,m,sy):
    """
    Set and generate strategy portfolio fullname
    Args:
        String: Symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    try:
        st = ''
        if sy =='ls': st = 'long/short'
        if sy =='s': st = 'ultra short'

        portf_symbol = set_portf_symbol()
        asset_class_id = ac
        market_id = m
        fullname = set_portf_fullname(portf_symbol, get_asset_class_name(ac), get_market_name(m), st)
        decimal_places = get_decimal_places(ac)
        pip = 1
        sector = 0
        unit = get_unit(m)
        portf_owner = set_portf_owner()
        portf_description = get_portf_description(ac,m,st,portf_owner)
        account_reference = 1000

        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
        "('"+ portf_symbol +"')"
        debug(sql)
        cr.execute(sql)
        connection.commit()
        sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
        "('"+ str(portf_symbol) +"','"+ str(fullname) +"','"+ str(asset_class_id) +"','"+ str(market_id) +"',"+ str(decimal_places) +","+ str(pip) +","+ str(sector) +",'"+ str(unit) +"','"+ str(portf_description) +"',"+ str(account_reference) +","+ str(portf_owner) +")"
        debug(sql)
        cr.execute(sql)
        connection.commit()

        gen_portf_allocation(portf_symbol,ac,m,sy)

        cr.close()
        connection.close()

    except Exception as e: debug(e)

def gen_portf():
    """
    Set and generate strategy portfolio fullname
    Args:
        String: Symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    try:

        #Scan Asset Class and create portfolio if not reach threshold
        min_portf_threshold = 200
        connection = pymysql.connect(host=db_srv,user=db_usr,password=db_pwd, db=db_name,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        cr = connection.cursor(pymysql.cursors.SSCursor)
        sql = "SELECT asset_class_id FROM asset_class WHERE asset_class_id <> 'PF:' AND asset_class_id <> 'MA:' AND asset_class_id <>'BD:' AND asset_class_id <>'CO:' "
        cr.execute(sql)
        rs = cr.fetchall()
        for row in rs:
            asset_class_id = row[0]
            if asset_class_id == 'CR:' or asset_class_id == 'FX:':
                market_id = 'GO>'
                for i in range(min_portf_threshold):
                    create_portf(asset_class_id,market_id, get_strategy() )
            else:
                cr_m = connection.cursor(pymysql.cursors.SSCursor)
                sql_m = "SELECT market_id FROM markets WHERE market_id <> 'GO>' "
                cr_m.execute(sql_m)
                rs_m = cr_m.fetchall()
                for row in rs_m:
                    market_id = row[0]
                    for i in range(min_portf_threshold):
                        create_portf(asset_class_id,market_id, get_strategy() )

        cr.close()
        cr_m.close()
        connection.close()

    except Exception as e: debug(e)

gen_portf()
