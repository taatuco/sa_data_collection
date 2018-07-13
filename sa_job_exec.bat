::###############################################################################
:: Desc: Batch to execute R and python script jobs related to data collection.
::
:: This batch file execute R script and Python script that is dedicated to
:: data collection and data manipulation on the SQL database.
::
:: Auth: dh@taatu.co (Taatu Ltd.)
:: Date: July 1, 2018
:: Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
::###############################################################################
SET SA_DATA_DIR="C:\xampp\htdocs\_sa\sa_data_collection"
SET LOGFILE="%SA_DATA_DIR%\sa_col_log.log"
SET _R_SCRIPT_EXE="C:\Program Files\R\R-3.5.0\bin\x64\Rscript.exe"
SET _PIP_EXE="C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\Scripts\pip.exe"
SET _PY_EXE="C:\Users\Administrator\AppData\Local\Programs\Python\Python36-32\python.exe"
call :Logit >> %LOGFILE%
exit /b 0

:Logit
:: Rscript that collect price_historical_data using quantmod library
DEL /F /Q "%SA_DATA_DIR%\r_quantmod\src\*"
%_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_quantmod\collect_data_r_quantmod.R"

:: Rscript that compute forecast points using ARIMA model using forecast library
DEL /F /Q "%SA_DATA_DIR%\r_forecast\src\*"
%_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_forecast\forecast_arima.R"

:: Install PyMySQL for Python to allow interaction with MySQL
%_PIP_EXE% install mysql-python
%_PIP_EXE% install PyMySQL

:: Install DateUtil for date and time format management
%_PIP_EXE% install python-dateutil

:: Import and update historical data
%_PY_EXE% "%SA_DATA_DIR%\r_quantmod\insert_db_price_data.py"

:: Compute TA data
%_PY_EXE% "%SA_DATA_DIR%\ta_data\ta_main_update_data.py"
