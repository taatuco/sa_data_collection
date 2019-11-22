REM Edt Configuration here #####################################################
@ECHO Due to sometimes Windows Environment Variables are not set properly
@ECHO For Python, pip etc... this is why it is recommended to run pip:
@ECHO invoking python.exe (python -m pip install requests) for instance

SET R_VER=R-3.5.1
SET PY_VER=Python37-32
SET SA_FRC_SCRIPT=%SYSTEMDRIVE%\smartalpha\sa_frc\get_forecast_data.bat
SET SA_FRC_DIR=%SYSTEMDRIVE%\smartalpha\sa_frc\

SET GET_DATA_TIME_ST=00:01
SET GET_NEWSDATA_TIME_0700_ST=07:00
SET GET_NEWSDATA_TIME_0730_ST=07:30
SET GET_NEWSDATA_TIME_0800_ST=08:00
SET GET_NEWSDATA_TIME_0815_ST=08:15
SET GET_NEWSDATA_TIME_0830_ST=08:30
SET GET_NEWSDATA_TIME_0845_ST=08:45
SET GET_NEWSDATA_TIME_0900_ST=09:00
SET GET_NEWSDATA_TIME_0915_ST=09:15
SET GET_NEWSDATA_TIME_0930_ST=09:30
SET GET_NEWSDATA_TIME_0945_ST=09:45
SET GET_NEWSDATA_TIME_1000_ST=10:00
SET GET_NEWSDATA_TIME_1015_ST=10:15
SET GET_NEWSDATA_TIME_1030_ST=10:30
SET GET_NEWSDATA_TIME_1045_ST=10:45
SET GET_NEWSDATA_TIME_1100_ST=11:00
SET GET_NEWSDATA_TIME_1115_ST=11:15
SET GET_NEWSDATA_TIME_1130_ST=11:30
SET GET_NEWSDATA_TIME_1145_ST=11:45
SET GET_NEWSDATA_TIME_1200_ST=12:00
SET GET_NEWSDATA_TIME_1215_ST=12:15
SET GET_NEWSDATA_TIME_1230_ST=12:30
SET GET_NEWSDATA_TIME_1245_ST=12:45
SET GET_NEWSDATA_TIME_1300_ST=13:00
SET GET_NEWSDATA_TIME_1315_ST=13:15
SET GET_NEWSDATA_TIME_1330_ST=13:30
SET GET_NEWSDATA_TIME_1345_ST=13:45
SET GET_NEWSDATA_TIME_1400_ST=14:00
SET GET_NEWSDATA_TIME_1415_ST=14:15
SET GET_NEWSDATA_TIME_1430_ST=14:30
SET GET_NEWSDATA_TIME_1445_ST=14:45
SET GET_NEWSDATA_TIME_1500_ST=15:00
SET GET_NEWSDATA_TIME_1515_ST=15:15
SET GET_NEWSDATA_TIME_1530_ST=15:30
SET GET_NEWSDATA_TIME_1545_ST=15:45
SET GET_NEWSDATA_TIME_1600_ST=16:00
SET GET_NEWSDATA_TIME_1615_ST=16:15
SET GET_NEWSDATA_TIME_1630_ST=16:30
SET GET_NEWSDATA_TIME_1645_ST=16:45
SET GET_NEWSDATA_TIME_1700_ST=17:00
SET GET_NEWSDATA_TIME_1715_ST=17:15
SET GET_NEWSDATA_TIME_1730_ST=17:30
SET GET_NEWSDATA_TIME_1745_ST=17:45
SET GET_NEWSDATA_TIME_1800_ST=18:00
SET GET_NEWSDATA_TIME_1815_ST=18:15
SET GET_NEWSDATA_TIME_1830_ST=18:30
SET GET_NEWSDATA_TIME_1845_ST=18:45
SET GET_NEWSDATA_TIME_1900_ST=19:00
SET GET_NEWSDATA_TIME_1915_ST=19:15
SET GET_NEWSDATA_TIME_1930_ST=19:30
SET GET_NEWSDATA_TIME_1945_ST=19:45
SET GET_NEWSDATA_TIME_2000_ST=20:00
SET GET_NEWSDATA_TIME_2015_ST=20:15
SET GET_NEWSDATA_TIME_2030_ST=20:30
SET GET_NEWSDATA_TIME_2045_ST=20:45
SET GET_NEWSDATA_TIME_2100_ST=21:00
SET GET_NEWSDATA_TIME_2115_ST=21:15
SET GET_NEWSDATA_TIME_2130_ST=21:30
SET GET_NEWSDATA_TIME_2145_ST=21:45
SET GET_NEWSDATA_TIME_2200_ST=22:00
SET GET_NEWSDATA_TIME_2215_ST=22:15
SET GET_NEWSDATA_TIME_2230_ST=22:30
SET GET_NEWSDATA_TIME_2245_ST=22:45
SET GET_NEWSDATA_TIME_2300_ST=23:00
REM ############################################################################

SET SA_DATA_DIR=%~dp0
SET RUN_DATA_COLLECT="%SA_DATA_DIR%_sa_collect_data.bat"
SET GET_DATA="%SA_DATA_DIR%sa_1_get_data.bat"
SET GET_FRC="%SA_DATA_DIR%sa_2_get_forecast.bat"
SET SET_FULLDATA="%SA_DATA_DIR%sa_3_set_fulldata.bat"
SET SET_DATA="%SA_DATA_DIR%sa_4_set_data.bat"
SET GET_NEWSDATA="%SA_DATA_DIR%sa_5_get_newsdata.bat"
SET GET_NEWSDATA_SPEC="%SA_DATA_DIR%sa_6_get_newsdata.bat"
SET PROCESS_MAIL_Q="%SA_DATA_DIR%sa_7_process_mail_q.bat"
SET REBUILD_DATA_SCRIPT_1="%SA_DATA_DIR%scripts\1_rebuild_data_collection.bat"
SET REBUILD_DATA_SCRIPT_2="%SA_DATA_DIR%scripts\2_rebuild_data_forecast.bat"
SET REBUILD_DATA_SCRIPT_3="%SA_DATA_DIR%scripts\3_rebuild_data_dataset.bat"
SET RECALC_FORCAST_MODEL="%SA_DATA_DIR%scripts\forecast_model_recalc.bat"
SET RECALC_INSTRUMENT="%SA_DATA_DIR%scripts\recalc_instrument.bat"

SET GET_QM_DATA="%SA_DATA_DIR%r_quantmod\get_quantmod_data.bat"
SET GET_OA_DATA="%SA_DATA_DIR%r_oanda\get_oanda_data.bat"
SET GET_CC_DATA="%SA_DATA_DIR%p_cryptocompare\get_cryptocompare_data.bat"

SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"

REM ### Setup default data
REM ### NOTE: REMOVE THIS BLOCK TO NOT OVERWRITE EXISTING DATA ###
REM %_PY_EXE% "%SA_DATA_DIR%lang\set_lang.py"
REM %_PY_EXE% "%SA_DATA_DIR%labels\set_labels.py"
REM %_PY_EXE% "%SA_DATA_DIR%labels\set_recomm_text_lang.py"
REM %_PY_EXE% "%SA_DATA_DIR%labels\set_email_templates.py"
REM %_PY_EXE% "%SA_DATA_DIR%labels\set_briefing_text_lang.py"
REM %_PY_EXE% "%SA_DATA_DIR%asset_class\set_asset_class.py"
REM %_PY_EXE% "%SA_DATA_DIR%markets\set_market.py"
REM %_PY_EXE% "%SA_DATA_DIR%sectors\set_sector.py"
REM %_PY_EXE% "%SA_DATA_DIR%newsdata\set_newsdata.py"
REM %_PY_EXE% "%SA_DATA_DIR%brokers\set_brokers.py"
REM %_PY_EXE% "%SA_DATA_DIR%users\set_users.py"
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
@ECHO CALL %GET_QM_DATA% >> %GET_DATA%
@ECHO CALL %GET_OA_DATA% >> %GET_DATA%
@ECHO CALL %GET_CC_DATA% >> %GET_DATA%

REM ### Quantmod
DEL /F /Q %GET_QM_DATA%
MKDIR "%SA_DATA_DIR%r_quantmod\src"
@ECHO DEL /F /Q "%SA_DATA_DIR%r_quantmod\src\*" > %GET_QM_DATA%
@ECHO %_R_SCRIPT_EXE% "%SA_DATA_DIR%r_quantmod\collect_data.R" >> %GET_QM_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%r_quantmod\insert_db_price_data.py" >> %GET_QM_DATA%

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
@ECHO CALL %SA_FRC_SCRIPT% >> %GET_FRC%

REM ### 3 Set Data
DEL /F /Q %SET_FULLDATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\collect_instr_fulldata.py" >> %SET_FULLDATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%portfolios\portf_main_get_data.py" >> %SET_FULLDATA%

REM ### 4 Set Data
DEL /F /Q %SET_DATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\collect_instr_data.py" >> %SET_DATA%

REM ### 5 Get NewsData Global
DEL /F /Q %GET_NEWSDATA%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\collect_news_data.py" >> %GET_NEWSDATA%

REM ### 6 Get NewsData Specific
DEL /F /Q %GET_NEWSDATA_SPEC%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\collect_news_data_spec_set.py" >> %GET_NEWSDATA_SPEC%

REM ### 7 Process email queue
DEL /F /Q %PROCESS_MAIL_Q%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\process_mail_queue.py" >> %PROCESS_MAIL_Q%

REM ### SA Collect Data
DEL /F /Q %RUN_DATA_COLLECT%
@ECHO CALL %GET_DATA% >> %RUN_DATA_COLLECT%
@ECHO CALL %GET_FRC% >> %RUN_DATA_COLLECT%
@ECHO CALL %SET_FULLDATA% >> %RUN_DATA_COLLECT%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\sa_logging.py" >> %RUN_DATA_COLLECT%

REM ### Data Rebuild Script
DEL /F %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO ########################################################################## >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO Rebuild the entire dataset prices, trades, forecast data >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO -------------------------------------------------------- >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO. >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO 1. Run 1_rebuild_data_collection to clear the existing data >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO 2. Run 2_rebuild_data_forecast to download the latest forecast data >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO 3. Run 3_rebuild_data_dataset to update all the related tables accordingly >> %REBUILD_DATA_SCRIPT_1%
@ECHO @ECHO ########################################################################## >> %REBUILD_DATA_SCRIPT_1%
@ECHO PAUSE >> %REBUILD_DATA_SCRIPT_1%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\_1_rebuild_instr_dataset.py" >> %REBUILD_DATA_SCRIPT_1%
@ECHO %GET_QM_DATA% >> %REBUILD_DATA_SCRIPT_1%
@ECHO %GET_AV_DATA% >> %REBUILD_DATA_SCRIPT_1%
@ECHO %GET_CC_DATA% >> %REBUILD_DATA_SCRIPT_1%
@ECHO %GET_OA_DATA% >> %REBUILD_DATA_SCRIPT_1%
DEL /F %REBUILD_DATA_SCRIPT_2%
@ECHO %SA_FRC_SCRIPT% >> %REBUILD_DATA_SCRIPT_2%
DEL /F %REBUILD_DATA_SCRIPT_3%
@ECHO %_PY_EXE% "%SA_DATA_DIR%core\_2_rebuild_instr_dataset.py" >> %REBUILD_DATA_SCRIPT_3%

REM ### Forecast Model Recalculation
DEL /F %RECALC_FORCAST_MODEL%
@ECHO @ECHO ########################################################################## >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO Recalculate Forecast Model and Score >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO -------------------------------------------------------- >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO. >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO 1. This script will include newly added model and recalculate score >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO 2. Run this during the Weekend to not affect the published signals >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO 3. This process might take long hours probably a day or a month >> %RECALC_FORCAST_MODEL%
@ECHO @ECHO ########################################################################## >> %RECALC_FORCAST_MODEL%
@ECHO PAUSE >> %RECALC_FORCAST_MODEL%
@ECHO %_PY_EXE% "%SA_FRC_DIR%get_prediction_model_fullset.py" >> %RECALC_FORCAST_MODEL%

REM ### Recalculation instrument data
DEL /F %RECALC_INSTRUMENT%
@ECHO @ECHO ########################################################################## >> %RECALC_INSTRUMENT%
@ECHO @ECHO Recalculate instruments prices/indicators and Forecast Model >> %RECALC_INSTRUMENT%
@ECHO @ECHO ------------------------------------------------------------ >> %RECALC_INSTRUMENT%
@ECHO @ECHO IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT >> %RECALC_INSTRUMENT%
@ECHO @ECHO. >> %RECALC_INSTRUMENT%
@ECHO @ECHO 1. Run the Py script: to update table price_instruments_data for specific symbol >> %RECALC_INSTRUMENT%
@ECHO @ECHO 2. Run the Py script: to compute forecast model and score for specific symbol >> %RECALC_INSTRUMENT%
@ECHO @ECHO 3. Run the Py script: to update price patterns for specific symbol >> %RECALC_INSTRUMENT%
@ECHO @ECHO 4. Run the Py script: to collect target_price for specific symbol >> %RECALC_INSTRUMENT%
@ECHO @ECHO ########################################################################## >> %RECALC_INSTRUMENT%
@ECHO PAUSE >> %RECALC_INSTRUMENT%
@ECHO %_PY_EXE% -m idlelib "%SA_DATA_DIR%core\collect_instr_fulldata_full_set_spec.py" >> %RECALC_INSTRUMENT%
@ECHO %_PY_EXE% -m idlelib "%SA_FRC_DIR%get_prediction_model_fullset_spec.py" >> %RECALC_INSTRUMENT%
@ECHO %_PY_EXE% -m idlelib "%SA_DATA_DIR%core\collect_instr_fulldata_full_set_spec.py" >> %RECALC_INSTRUMENT%
@ECHO %_PY_EXE% -m idlelib "%SA_FRC_DIR%get_prediction_model_fullset_spec.py" >> %RECALC_INSTRUMENT%

REM ### Set Schedule tasks
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_DATA /TR %RUN_DATA_COLLECT% /RI 0 /ST %GET_DATA_TIME_ST% /F

REM ### SET NewsData collection
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_05 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0700_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_06 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0730_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_07 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0800_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_071 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0815_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_08 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0830_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_081 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0845_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_09 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0900_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_091 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0915_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_10 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0930_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_101 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_0945_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_11 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1000_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_111 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1015_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_12 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1030_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_121 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1045_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_13 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1100_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_131 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1115_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_14 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1130_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_141 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1145_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_15 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1200_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_151 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1215_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_16 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1230_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_161 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1245_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_17 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1300_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_171 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1315_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_18 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1330_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_181 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1345_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_19 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1400_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_191 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1415_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_20 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1430_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_201 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1445_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_21 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1500_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_211 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1515_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_22 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1530_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_221 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1545_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_23 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1600_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_231 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1615_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_24 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1630_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_241 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1645_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_25 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1700_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_251 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1715_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_26 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1730_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_261 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1745_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_27 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1800_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_271 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1815_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_28 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1830_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_281 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1845_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_29 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_1900_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_291 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1915_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_30 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1930_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_301 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_1945_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_31 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_2000_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_311 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2015_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_32 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2030_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_321 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2045_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_33 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_2100_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_331 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2115_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_34 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2130_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_341 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2145_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_35 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_2200_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_351 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2215_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_36 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2230_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_361 /TR %GET_NEWSDATA% /RI 0 /ST %GET_NEWSDATA_TIME_2245_ST% /F
SCHTASKS /Create /SC DAILY /TN SMARTALPHA_GET_NEWSDATA_37 /TR %GET_NEWSDATA_SPEC% /RI 0 /ST %GET_NEWSDATA_TIME_2300_ST% /F

REM Process mail queue
SCHTASKS /Create /SC MINUTE /MO 1 /TN SMARTALPHA_PROCESS_MAIL_Q /TR %PROCESS_MAIL_Q% /F
