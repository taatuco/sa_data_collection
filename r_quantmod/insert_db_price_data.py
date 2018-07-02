###############################################################################
# Desc: Read csv and update the database accordingly: table: price_historical_data
#
# Read csv file and insert records that are not existing in the database table
# price_instruments_data. (Avoid duplicate records).
#
# Dependencies: PyMySQL is required to access MySQL database.
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
###############################################################################

#define database username and password and other variable regarding access to db
db_usr = 'sa_db_user'
db_pwd = '9XHWVxTH9ZJnshvN'
db_name = 'smartalpha'
db_srv = 'localhost'

# Use csv and file system
import csv
csvdir = "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_quantmod\\src\\"
from pathlib import Path

# Use PyMySQL to access MySQL database
import pymysql.cursors

connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Get symbol_list to iterate for records to collect
try:
    with connection.cursor() as cursor:
        # Read symbol_list
        sql = "SELECT * FROM symbol_list"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            symbol_quantmod = row["r_quantmod"]
            symbol_index = row["symbol"]
            file_str = csvdir+symbol_quantmod+'.csv'
            filepath = Path(file_str)
            if filepath.exists():
                # Read csv file
                with open(file_str) as csvfile:
                    readCSV = csv.reader(csvfile, delimiter=',')
                    for row in readCSV:
                        # For each symbol, retrieve the csv content
                        price_date = row[0]
                    
                        price_date = price_date.replace('.', '-')
                        price_date = price_date.replace('X', '')
                        price_date = price_date.replace('-','')
                        price_date = '%.8s' % price_date
                        price_open = row[1]
                        price_high = row[2]
                        price_low = row[3]
                        price_close = row[4]
                        volume = row[5]
                        # check for each row if not already exists.
                        # if exists, then insert new record, else ignore.
                        if price_open != "open":
                            with connection.cursor() as query_count_cursor:
                                query_count_sql = "SELECT * FROM price_instruments_data WHERE symbol='"+symbol_index+"' AND 'date'='"+price_date+"'"
                                query_count_cursor.execute(query_count_sql)
                                exists_rec = query_count_cursor.fetchone()
                        
                            if not exists_rec:
                                # insert record in case not existing.
                                with connection.cursor() as query_insert_cursor:
                                    insert_price_sql = "INSERT INTO price_instruments_data (symbol, date, price_close, price_open, price_low, price_high, volume) VALUES ('"+symbol_index+"',"+price_date+","+price_close+","+price_open+","+price_low+","+price_high+","+volume+");"
                                    #print(insert_price_sql)
                                    query_insert_cursor.execute(insert_price_sql)
                                    connection.commit()

finally:
    connection.close()
