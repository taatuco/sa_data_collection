::###############################################################################
:: Desc: Batch to execute R and python script jobs related to data collection.
::
:: This batch file execute R script and Python script that is dedicated to
:: data collection and data manipulation on the SQL database.
::
:: Dependencies: Required Python 3.X, R x64 3.X
::
:: Auth: dh@taatu.co (Taatu Ltd.)
:: Date: July 1, 2018
:: Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
::###############################################################################

:: Rscript that collect price_historical_data using quantmod library
DEL /F /Q "C:\xampp\htdocs\_sa\sa_data_collection\r_quantmod\src\*"
"C:\Program Files\R\R-3.5.0\bin\x64\Rscript.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_quantmod\collect_data_r_quantmod.R"

:: Rscript that compute forecast points using ARIMA model using forecast library
DEL /F /Q "C:\xampp\htdocs\_sa\sa_data_collection\r_forecast\src\*"
"C:\Program Files\R\R-3.5.0\bin\x64\Rscript.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_forecast\forecast_arima.R"

:: Install PyMySQL for Python to allow interaction with MySQL
"C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe" install mysql-python
"C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe" install PyMySQL

:: Install DateUtil for date and time format management
"C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe" install python-dateutil

:: Import and update historical data
"C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_quantmod\insert_db_price_data.py"
:: Import forecast price point
"C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_forecast\insert_db_forecast_data.py"

:: Compute TA data
"C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe" "C:\xampp\htdocs\_sa\sa_data_collection\ta_data\ta_main_update_data.py"
