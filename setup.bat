REM Edit and Set version here ##################################################
SET R_VER=R-3.5.0
SET PY_VER=Python36-32
SET PY_BS=beautifulsoup4
REM ############################################################################

SET SA_DATA_DIR=%~dp0
SET GET_DATA="%SA_DATA_DIR%sa_1_get_data.bat"
SET GET_FRC="%SA_DATA_DIR%sa_2_get_forecast.bat"
SET SET_DATA="%SA_DATA_DIR%sa_3_set_data.bat"

SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"

REM ### 1 Get Data
@ECHO %_PY_EXE% -m pip install --upgrade pip > %GET_DATA%
@ECHO %_PIP_EXE% install mysql-python >> %GET_DATA%
@ECHO %_PIP_EXE% install PyMySQL >> %GET_DATA%
@ECHO %_PIP_EXE% install python-dateutil >> %GET_DATA%
@ECHO %_PIP_EXE% install %PY_BS% >> %GET_DATA%
@ECHO %_PY_EXE% -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose >> %GET_DATA%

@ECHO START "" "%SA_DATA_DIR%r_quantmod\get_quantmod_data.bat" >> %GET_DATA%
@ECHO START "" "%SA_DATA_DIR%r_oanda\get_oanda_data.bat" >> %GET_DATA%

REM ### Quantmod
SET GET_QM_DATA="%SA_DATA_DIR%r_quantmod\get_quantmod_data.bat"
@ECHO DEL /F /Q "%SA_DATA_DIR%r_quantmod\src\*" > %GET_QM_DATA%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_quantmod\collect_data.R" >> %GET_QM_DATA%
@ECHO START "" %_PY_EXE% "%SA_DATA_DIR%r_quantmod\insert_db_price_data_asc.py" >> %GET_QM_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%r_quantmod\insert_db_price_data_dsc.py" >> %GET_QM_DATA%

REM ### Oanda
SET GET_OA_DATA="%SA_DATA_DIR%r_oanda\get_oanda_data.bat"
@ECHO DEL /F /Q "%SA_DATA_DIR%r_oanda\src\*" > %GET_OA_DATA%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_oanda\collect_data.R" >> %GET_OA_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%r_oanda\insert_db_price_data.py" >> %GET_OA_DATA%

REM ### 2 Get Forecast
@ECHO DEL /F /Q "%SA_DATA_DIR%r_forecast\src\*" > %GET_FRC%
@ECHO START "" %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_forecast\forecast_arima_asc.R" >> %GET_FRC%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_forecast\forecast_arima_dsc.R" >> %GET_FRC%

REM ### 3 Set Data
@ECHO %_PY_EXE% "%SA_DATA_DIR%data\ta_main_update_data.py" >> %SET_DATA%
