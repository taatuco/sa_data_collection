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

# Use csv
import csv
csvdir = "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_quantmod\\src\\"

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
            # Read csv file
            with open(csvdir+symbol_quantmod+'.csv') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                for row in readCSV:
                    # For each symbol, retrieve the csv content
                    price_date = row[0]
                    price_date = price_date.replace('.', '-')
                    price_date = price_date.replace('X', '')
                    price_query_date = price_date.replace('-','')
                    price_query_date = '%.8s' % price_query_date
                    price_open = row[1]
                    price_high = row[2]
                    price_low = row[3]
                    price_close = row[4]
                    volume = row[5]
                    # check for each row if not already exists.
                    # if exists, then insert new record, else ignore.
                    with connection.cursor() as query_count_cursor:
                        query_count_cursor.execute("SELECT * FROM price_instruments_data")
                        #query_count_cursor.execute("SELECT COUNT(*) FROM price_instruments_data WHERE symbol='"+symbol_index+"' AND date='"+price_query_date+"'")
                        #print(price_query_date, symbol_index)
                        # gets the number of rows affected by the command executed
                        price_instruments_data_count = query_count_cursor.rowcount
                        print(price_instruments_data_count)
                    #if price_instruments_data_count == 0:
                        # insert record in case not existing.
                        #with connection.cursor() as cursor:
                            #sql_insert_price = "INSERT INTO price_instruments_data (symbol, date, price_close, price_open, price_low, price_high, volume) VALUES ("+symbol_index+","+price_date+","+price_close+","+price_open+","+price_low+","+price_high+","+volume+");"
                            #cursor.execute()
                        # commit query...
                        #connection.commit()
finally:
    connection.close()