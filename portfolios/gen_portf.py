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
    res = cursor.fetchall()
    for row in res:
        symbol = symbol + row[0]

    symbol = symbol + str(random.randint(1, 999))
    ret = get_portf_suffix() + symbol.upper()
    cursor.close()
    connection.close()
    return ret

def set_portf_fullname(symbol, asset_class, market, strategy_type):
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
    fullname = symbol.replace(get_portf_suffix(), '')
    ret = fullname + ' ' + market + ' ' + asset_class + ' ' + strategy_type
    return ret

def get_nickname(uid):
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
    sql = "SELECT nickname FROM users WHERE id="+ str(uid)
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    cursor.close()
    connection.close()
    return ret

def get_portf_description(asset_class, market, strategy_type, uid):
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
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT portf_description FROM labels WHERE lang = '"+ "en" +"'"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        portf_description = row[0]

    nickname = get_nickname(uid)
    market_asset_class = asset_class + ' ' + market + ' '+ strategy_type
    portf_description = portf_description.replace('{market_asset_class}', market_asset_class)
    portf_description = portf_description.replace('{nickname}', nickname)
    ret = portf_description
    cursor.close()
    connection.close()
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
    res = cursor.fetchall()
    for row in res:
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
    sql = "SELECT asset_class_name FROM asset_class WHERE asset_class_id='"+\
    str(asset_class_id) +"' "
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
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT market_label FROM markets WHERE market_id='"+ str(market_id) +"' "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
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
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT decimal_places FROM instruments WHERE asset_class = '"+\
    str(asset_class_id) +"' ORDER BY decimal_places DESC LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    return ret

def get_unit(market_id):
    """
    Get unit used by the strategy portfolio
    Args:
        String: Market id
    Returns:
        String: Unit according to market provided by arg.
    """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT currency_code FROM markets WHERE market_id = '"+ str(market_id) +"' "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    return ret

def set_portf_owner():
    """
    Get a random owner for the portfolio from selection in table users
    tagged as bot for use as example strategy portfolio.
    Args:
        None
    Returns:
        String: username
    """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT id FROM users WHERE is_bot=1 ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    return ret

def select_allocation(asset_class, market):
    """
    Select an allocation for the strategy portfolio. Get an instrument
    out from a random selection as per provided asset class or market
    Args:
        String: Asset class
        String: Market
    Returns:
        String: instrument symbol
    """
    ret = ''
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "SELECT symbol FROM instruments WHERE symbol NOT LIKE '%"+\
    get_portf_suffix() +"%' AND asset_class = '"+ str(asset_class) +\
    "' AND market = '"+ str(market) +"' ORDER BY RAND() LIMIT 1"
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        ret = row[0]
    return ret

def gen_portf_allocation(symbol, asset_class, market, strategy_type):
    """
    Set and generate an allocation for the strategy portfolio according
    to arguments provided. Insert in database.
    Args:
        String: Strategy portfolio symbol
        String: Asset class
        String: Market
        String: The type of strategy (Long, Short, Long/Short)
    Returns:
        None
    """
    strategy_order_type = 'long/short'
    if strategy_type == 'l':
        strategy_order_type = 'long'
    if strategy_type == 's':
        strategy_order_type = 'short'
    strategy_conviction = 'neutral'

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)

    sql = "INSERT IGNORE INTO portfolios(portf_symbol, symbol, quantity, "+\
    "strategy_order_type, strategy_conviction) VALUES "+\
    "('"+ str(symbol) +"','"+ select_allocation(asset_class, market) +\
    "',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
    "('"+ str(symbol) +"','"+ select_allocation(asset_class, market) +\
    "',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
    "('"+ str(symbol) +"','"+ select_allocation(asset_class, market) +\
    "',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
    "('"+ str(symbol) +"','"+ select_allocation(asset_class, market) +\
    "',1,'"+ strategy_order_type +"','"+ strategy_conviction +"'),"+\
    "('"+ str(symbol) +"','"+ select_allocation(asset_class, market) +\
    "',1,'"+ strategy_order_type +"','"+ strategy_conviction +"')"
    debug(sql)
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()

def create_portf(asset_class, market, strategy_type_abr):
    """
    Create the strategy portfolioby inserting data into symbol_list and
    instruments.
    Args:
        String: Asset_class
        String: Market
        String: The type of strategy (Long (l), Short (s), Long/Short (ls): abreviation)
    Returns:
        String: A strategy portfolio fullname according to provided args.
    """
    strategy_type = ''
    if strategy_type_abr == 'ls':
        strategy_type = 'long/short'
    if strategy_type_abr == 's':
        strategy_type = 'ultra short'

    portf_symbol = set_portf_symbol()
    asset_class_id = asset_class
    market_id = market
    fullname = set_portf_fullname(portf_symbol,
                                  get_asset_class_name(asset_class),
                                  get_market_name(market), strategy_type)
    decimal_places = get_decimal_places(asset_class)
    pip = 1
    sector = 0
    unit = get_unit(market)
    portf_owner = set_portf_owner()
    portf_description = get_portf_description(asset_class, market, strategy_type, portf_owner)
    account_reference = 1000

    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    sql = "INSERT IGNORE INTO symbol_list(symbol) VALUES "+\
    "('"+ portf_symbol +"')"
    debug(sql)
    cursor.execute(sql)
    connection.commit()
    sql = "INSERT IGNORE INTO instruments(symbol, fullname, asset_class, market, "+\
    "decimal_places, pip, sector, unit, description, account_reference, owner) VALUES "+\
    "('"+ str(portf_symbol) +"','"+ str(fullname) +"','"+ str(asset_class_id) +"','"+\
    str(market_id) +"',"+ str(decimal_places) +","+ str(pip) +","+ str(sector) +",'"+\
    str(unit) +"','"+ str(portf_description) +"',"+ str(account_reference) +","+\
    str(portf_owner) +")"
    debug(sql)
    cursor.execute(sql)
    connection.commit()

    gen_portf_allocation(portf_symbol, asset_class, market, strategy_type_abr)

    cursor.close()
    connection.close()

def gen_alt_portf(asset_class_id, market_id, strategy_type, min_portf_threshold):
    """
    Create and generate alternative portfolio based on market.
    Strategy portfolio that are generated are used as example.
    Args:
        None
    Returns:
        Int: Number of generated strategy portfolio
    """
    ret = 0
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cr_m = connection.cursor(pymysql.cursors.SSCursor)
    sql_m = "SELECT market_id FROM markets WHERE market_id <> 'GO>' "
    cr_m.execute(sql_m)
    rs_m = cr_m.fetchall()
    for row in rs_m:
        market_id = row[0]
        for i in range(min_portf_threshold):
            create_portf(asset_class_id, market_id, strategy_type)
            ret = i
    cr_m.close()
    connection.close()
    return ret

def gen_portf():
    """
    Scan Asset Class and create portfolio if not reach threshold.
    Auto-generated strategy portfolio are used as examples.
    Args:
        None
    Returns:
        Int: Number of generated strategy portfolio
    """
    ret = 0
    min_portf_threshold = 200
    connection = pymysql.connect(host=DB_SRV,
                                 user=DB_USR,
                                 password=DB_PWD,
                                 db=DB_NAME,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor(pymysql.cursors.SSCursor)
    strategy_type = get_strategy()
    sql = "SELECT asset_class_id FROM asset_class WHERE asset_class_id <> 'PF:' "+\
    "AND asset_class_id <> 'MA:' AND asset_class_id <>'BD:' AND asset_class_id <>'CO:' "
    cursor.execute(sql)
    res = cursor.fetchall()
    for row in res:
        asset_class_id = row[0]
        if asset_class_id == 'CR:' or asset_class_id == 'FX:':
            market_id = 'GO>'
            for i in range(min_portf_threshold):
                create_portf(asset_class_id, market_id, strategy_type)
                ret = i
        else:
            gen_alt_portf(asset_class_id, market_id, strategy_type, min_portf_threshold)
    cursor.close()
    connection.close()
    return ret

gen_portf()
