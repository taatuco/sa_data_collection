REM Edt Configuration here #####################################################
SET R_VER=R-3.5.1
SET PY_VER=Python37-32
SET PY_BS=beautifulsoup4
SET EXPRESS_JS=express

SET GET_DATA_TIME_ST=01:00
SET GET_DATA_TIME_ET=04:00
SET GET_FRC_TIME_ST=05:00
SET GET_FRC_TIME_ET=08:00
SET SET_DATA_TIME_ST=09:00
SET SET_DATA_TIME_ET=12:00
REM ############################################################################

SET SA_DATA_DIR=%~dp0
SET API_DIR=%SA_DATA_DIR%api
SET GET_DATA="%SA_DATA_DIR%sa_1_get_data.bat"
SET GET_FRC="%SA_DATA_DIR%sa_2_get_forecast.bat"
SET SET_DATA="%SA_DATA_DIR%sa_3_set_data.bat"

SET GET_QM_DATA="%SA_DATA_DIR%r_quantmod\get_quantmod_data.bat"
SET GET_OA_DATA="%SA_DATA_DIR%r_oanda\get_oanda_data.bat"
SET GET_CC_DATA="%SA_DATA_DIR%p_cryptocompare\get_cryptocompare_data.bat"


SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"
SET _NODE=node
SET _NPM=npm

REM ### Setup Node.js and express.js
cd %API_DIR%
CALL %_NPM% install %EXPRESS_JS% --save

REM ### To start Node.js server

REM ### Setup default data
%_PY_EXE% "%SA_DATA_DIR%lang\set_lang.py"


REM ### 1 Get Data
DEL /F /Q %GET_DATA%
MKDIR "%API_DIR%"
MKDIR "%API_DIR%\src"
@ECHO %_PY_EXE% -m pip install --upgrade pip > %GET_DATA%
@ECHO %_PIP_EXE% install mysql-python >> %GET_DATA%
@ECHO %_PIP_EXE% install PyMySQL >> %GET_DATA%
@ECHO %_PIP_EXE% install python-dateutil >> %GET_DATA%
@ECHO %_PIP_EXE% install %PY_BS% >> %GET_DATA%
@ECHO %_PY_EXE% -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose >> %GET_DATA%
@ECHO START "" %GET_QM_DATA% >> %GET_DATA%
@ECHO START "" %GET_OA_DATA% >> %GET_DATA%
@ECHO START "" %GET_CC_DATA% >> %GET_DATA%

REM ### Quantmod
DEL /F /Q %GET_QM_DATA%
MKDIR "%SA_DATA_DIR%r_quantmod\src"
@ECHO DEL /F /Q "%SA_DATA_DIR%r_quantmod\src\*" > %GET_QM_DATA%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_quantmod\collect_data.R" >> %GET_QM_DATA%
@ECHO START "" %_PY_EXE% "%SA_DATA_DIR%r_quantmod\insert_db_price_data_asc.py" >> %GET_QM_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%r_quantmod\insert_db_price_data_dsc.py" >> %GET_QM_DATA%

REM ### Oanda
DEL /F /Q %GET_OA_DATA%
MKDIR "%SA_DATA_DIR%r_oanda\src"
@ECHO DEL /F /Q "%SA_DATA_DIR%r_oanda\src\*" > %GET_OA_DATA%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_oanda\collect_data.R" >> %GET_OA_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%r_oanda\insert_db_price_data.py" >> %GET_OA_DATA%

REM ### Cryptocompare
@ECHO %_PY_EXE% "%SA_DATA_DIR%p_cryptocompare\collect_crypto_data.py" > %GET_CC_DATA%

REM ### 2 Get Forecast
DEL /F /Q %GET_FRC%
@ECHO START "" %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_forecast\forecast_arima_asc.R" >> %GET_FRC%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_forecast\forecast_arima_dsc.R" >> %GET_FRC%

REM ### 3 Set Data
DEL /F /Q %SET_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%w_signals\ta_main_update_data.py" >> %SET_DATA%

REM ### Set Schedule tasks
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_DATA% /RI 0 /ST %GET_DATA_TIME_ST% /ET %GET_DATA_TIME_ET% /K /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_FORECAST /TR %GET_FRC% /RI 0 /ST %GET_FRC_TIME_ST% /ET %GET_FRC_TIME_ET% /K /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_SET_DATA /TR %SET_DATA% /RI 0 /ST %SET_DATA_TIME_ST% /ET %SET_DATA_TIME_ET% /K /F
