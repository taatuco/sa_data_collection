REM Edt Configuration here #####################################################
SET R_VER=R-3.5.1
SET PY_VER=Python37-32
SET SA_FRC_SCRIPT=%SYSTEMDRIVE%\smartalpha\sa_frc\get_forecast_data.bat

SET GET_DATA_TIME_ST=00:01
SET GET_FRC_TIME_ST=01:00
SET GET_FULLDATA_TIME_ST=03:00
SET GET_NEWSDATA_TIME_0500_ST=05:00
SET GET_NEWSDATA_TIME_0530_ST=05:30
SET GET_NEWSDATA_TIME_0600_ST=06:00
SET GET_NEWSDATA_TIME_0630_ST=06:30
SET GET_NEWSDATA_TIME_0700_ST=07:00
SET GET_NEWSDATA_TIME_0730_ST=07:30
SET GET_NEWSDATA_TIME_0800_ST=08:00
SET GET_NEWSDATA_TIME_0830_ST=08:30
SET GET_NEWSDATA_TIME_0900_ST=09:00
SET GET_NEWSDATA_TIME_0930_ST=09:30
SET GET_NEWSDATA_TIME_1000_ST=10:00
SET GET_NEWSDATA_TIME_1030_ST=10:30
SET GET_NEWSDATA_TIME_1100_ST=11:00
SET GET_NEWSDATA_TIME_1130_ST=11:30
SET GET_NEWSDATA_TIME_1200_ST=12:00
SET GET_NEWSDATA_TIME_1230_ST=12:30
SET GET_NEWSDATA_TIME_1300_ST=13:00
SET GET_NEWSDATA_TIME_1330_ST=13:30
SET GET_NEWSDATA_TIME_1400_ST=14:00
SET GET_NEWSDATA_TIME_1430_ST=14:30
SET GET_NEWSDATA_TIME_1500_ST=15:00
SET GET_NEWSDATA_TIME_1530_ST=15:30
SET GET_NEWSDATA_TIME_1600_ST=16:00
SET GET_NEWSDATA_TIME_1630_ST=16:30
SET GET_NEWSDATA_TIME_1700_ST=17:00
SET GET_NEWSDATA_TIME_1730_ST=17:30
SET GET_NEWSDATA_TIME_1800_ST=18:00
SET GET_NEWSDATA_TIME_1830_ST=18:30
SET GET_NEWSDATA_TIME_1900_ST=19:00
SET GET_NEWSDATA_TIME_1930_ST=19:30
SET GET_NEWSDATA_TIME_2000_ST=20:00
SET GET_NEWSDATA_TIME_2030_ST=20:30
SET GET_NEWSDATA_TIME_2100_ST=21:00
SET GET_NEWSDATA_TIME_2130_ST=21:30
SET GET_NEWSDATA_TIME_2200_ST=22:00
SET GET_NEWSDATA_TIME_2230_ST=22:30
SET GET_NEWSDATA_TIME_2300_ST=23:00
SET GET_NEWSDATA_TIME_2330_ST=23:30
REM ############################################################################

SET SA_DATA_DIR=%~dp0
SET GET_DATA="%SA_DATA_DIR%sa_1_get_data.bat"
SET GET_FRC="%SA_DATA_DIR%sa_2_get_forecast.bat"
SET SET_FULLDATA="%SA_DATA_DIR%sa_3_set_fulldata.bat"
SET SET_DATA="%SA_DATA_DIR%sa_4_set_data.bat"
SET GET_NEWSDATA="%SA_DATA_DIR%sa_5_get_newsdata.bat"

SET GET_QM_DATA="%SA_DATA_DIR%r_quantmod\get_quantmod_data.bat"
SET GET_OA_DATA="%SA_DATA_DIR%r_oanda\get_oanda_data.bat"
SET GET_CC_DATA="%SA_DATA_DIR%p_cryptocompare\get_cryptocompare_data.bat"
SET GET_AV_DATA="%SA_DATA_DIR%p_alphavantage\get_alphavantage_data.bat"

SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"

REM ### Setup default data
REM ### NOTE: REMOVE THIS BLOCK TO NOT OVERWRITE EXISTING DATA ###
REM %_PY_EXE% "%SA_DATA_DIR%lang\set_lang.py"
REM %_PY_EXE% "%SA_DATA_DIR%labels\set_labels.py"
REM %_PY_EXE% "%SA_DATA_DIR%labels\set_recomm_text_lang.py"
REM %_PY_EXE% "%SA_DATA_DIR%labels\set_briefing_text_lang.py"
REM %_PY_EXE% "%SA_DATA_DIR%asset_class\set_asset_class.py"
REM %_PY_EXE% "%SA_DATA_DIR%markets\set_market.py"
REM %_PY_EXE% "%SA_DATA_DIR%sectors\set_sector.py"
REM %_PY_EXE% "%SA_DATA_DIR%newsdata\set_newsdata.py"
REM %_PY_EXE% "%SA_DATA_DIR%users\set_users.py"
REM %_PY_EXE% "%SA_DATA_DIR%portfolios\set_portf.py"
REM %_PY_EXE% "%SA_DATA_DIR%portfolios\set_strat.py"
REM %_PY_EXE% "%SA_DATA_DIR%portfolios\gen_portf.py"

REM ### 1 Get Data
DEL /F /Q %GET_DATA%
MKDIR "%SA_DATA_DIR%src"
@ECHO %_PY_EXE% -m pip install --upgrade pip > %GET_DATA%
@ECHO %_PIP_EXE% install mysql-python >> %GET_DATA%
@ECHO %_PIP_EXE% install PyMySQL >> %GET_DATA%
@ECHO %_PIP_EXE% install python-dateutil >> %GET_DATA%
@ECHO %_PIP_EXE% install beautifulsoup4 >> %GET_DATA%
@ECHO %_PIP_EXE% install requests >> %GET_DATA%
@ECHO %_PIP_EXE% install feedparser >> %GET_DATA%
@ECHO %_PIP_EXE% install vaderSentiment >> %GET_DATA%
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
@ECHO exit >> %GET_QM_DATA%

REM ### Oanda
DEL /F /Q %GET_OA_DATA%
MKDIR "%SA_DATA_DIR%r_oanda\src"
@ECHO DEL /F /Q "%SA_DATA_DIR%r_oanda\src\*" > %GET_OA_DATA%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_oanda\collect_data.R" >> %GET_OA_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%r_oanda\insert_db_price_data.py" >> %GET_OA_DATA%
@ECHO exit >> %GET_OA_DATA%

REM ### Cryptocompare
@ECHO %_PY_EXE% "%SA_DATA_DIR%p_cryptocompare\collect_crypto_data.py" > %GET_CC_DATA%
@ECHO exit >> %GET_CC_DATA%

REM ### Alphavantage
@ECHO %_PIP_EXE% install alpha_vantage > %GET_AV_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%p_alphavantage\collect_stocks_data.py" >> %GET_AV_DATA%
@ECHO exit >> %GET_AV_DATA%

REM ### 2 Get Forecast
DEL /F /Q %GET_FRC%
@ECHO START "" "%SA_FRC_SCRIPT%" >> %GET_FRC%

REM ### 3 Set Data
DEL /F /Q %SET_FULLDATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\collect_instr_fulldata.py" >> %SET_FULLDATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%portfolios\portf_main_get_data.py" >> %SET_FULLDATA%
@ECHO exit >> %SET_FULLDATA%

REM ### 4 Set Data
DEL /F /Q %SET_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\collect_instr_data.py" >> %SET_DATA%
@ECHO exit >> %SET_DATA%

REM ### 5 Get NewsData
DEL /F /Q %GET_NEWSDATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\collect_news_data.py" >> %GET_NEWSDATA%
@ECHO exit >> %GET_NEWSDATA%

REM ### Set Schedule tasks
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_DATA% /RI 0 /ST %GET_DATA_TIME_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_FORECAST /TR %GET_FRC% /RI 0 /ST %GET_FRC_TIME_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_SET_FULLDATA /TR %SET_FULLDATA% /RI 0 /ST %SET_FULLDATA_TIME_ST% /F

REM ### SET NewsData collection
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0500_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0530_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0600_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0630_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0700_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0730_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0800_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0830_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0900_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0930_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1000_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1030_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1100_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1130_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1200_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1230_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1300_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1330_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1400_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1430_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1500_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1530_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1600_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1630_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1700_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1730_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1800_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1830_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1900_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1930_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2000_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2030_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2100_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2130_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2200_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2230_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2300_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2330_ST% /F
