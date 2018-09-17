:: Batch: data collection

SET R_VER=R-3.5.0
SET PY_VER=Python36-32
SET PY_BS=beautifulsoup4

SET SA_DATA_DIR=C:\xampp\htdocs\_sa\sa_data_collection
SET LOGFILE="%SA_DATA_DIR%\sa_col_log.log"
SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"
call :Logit >> %LOGFILE%
exit /b 0

:Logit
:: Update and install various libraries
%_PY_EXE% -m pip install --upgrade pip
%_PIP_EXE% install mysql-python
%_PIP_EXE% install PyMySQL
%_PIP_EXE% install python-dateutil
%_PIP_EXE% install %PY_BS%

:: Collect price_historical_data from various sources
DEL /F /Q "%SA_DATA_DIR%\r_quantmod\src\*"
%_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_quantmod\collect_data.R"
%_PY_EXE% "%SA_DATA_DIR%\r_quantmod\insert_db_price_data.py"

DEL /F /Q "%SA_DATA_DIR%\r_oanda\src\*"
%_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_oanda\collect_data.R"
%_PY_EXE% "%SA_DATA_DIR%\r_oanda\insert_db_price_data.py"

:: Compute forecast points
DEL /F /Q "%SA_DATA_DIR%\r_forecast\src\*"
%_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_forecast\forecast_arima.R"

:: Compute TA data
%_PY_EXE% "%SA_DATA_DIR%\ta_data\ta_main_update_data.py"
