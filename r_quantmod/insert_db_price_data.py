###############################################################################
# Desc: Read csv and update the database accordingly: table: price_historical_data
#
# Read csv file and insert records that are not existing in the database table
# price_historical_data. (Avoid duplicate records).
#
# Dependencies: sqlalchemy is required to access MySQL database.
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
###############################################################################

#define database username and password.
db_usr = 'sa_db_user'
db_pwd = '9XHWVxTH9ZJnshvN'
db_engine = 'mysql://'+db_usr+':'+db_pwd+'@localhost/smartalpha'

# Use sqlalchemy to access MySQL database
from sqlalchemy import create_engine
engine = create_engine(db_engine)
symbol_list = sessionmaker(bind=engine)
symbol_list = symbol_list()

# Get symbol_list to iterate for records to collect
try:
    symbol_list.execute("""select * from symbol_list""")
    symbol_list.commit()

except:
    print symbol_list
finally:
    symbol_list.close()

# Read csv file

# For each symbol, retrieve the csv content
