::###############################################################################
:: Desc: Batch to execute R and python script jobs related to data collection.
::
:: This batch file execute R script and Python script that is dedicated to
:: data collection and data manipulation on the SQL database.
::
:: Auth: dh@taatu.co (Taatu Ltd.)
::
::###############################################################################

:: Rscript that collect price_historical_data using quantmod library
DEL /F /Q "C:\xampp\htdocs\_sa\sa_data_collection\r_quantmod\src\*"
"C:\Program Files\R\R-3.5.0\bin\x64\Rscript.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_quantmod\collect_data_r_quantmod.R"

:: Rscript that compute forecast points using ARIMA model using forecast library
DEL /F /Q "C:\xampp\htdocs\_sa\sa_data_collection\r_forecast\src\*"
"C:\Program Files\R\R-3.5.0\bin\x64\Rscript.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_forecast\forecast_arima.R"

:: Install SQLAlchemy for Python to allow interaction with MySQL 
"C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe" install SQLAlchemy
