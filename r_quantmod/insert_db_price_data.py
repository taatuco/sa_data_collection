###############################################################################
# Desc: Read csv and update the database accordingly: table: price_historical_data
#
# Read csv file and insert records that are not existing in the database table
# price_historical_data. (Avoid duplicate records).
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

# Use PyMySQL to access MySQL database
connection = pymysql.connect(host=db_srv,
                             user=db_usr,
                             password=db_pwd,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Get symbol_list to iterate for records to collect
try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM symbol_list"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    connection.close()

# Read csv file

# For each symbol, retrieve the csv content
