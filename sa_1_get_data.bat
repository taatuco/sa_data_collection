:: Batch: data collection

SET R_VER=R-3.5.0
SET PY_VER=Python36-32
SET PY_BS=beautifulsoup4

SET SA_DATA_DIR=C:\xampp\htdocs\_sa\sa_data_collection
SET LOGFILE="%SA_DATA_DIR%\sa_col_log.log"
SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"

:: Update and install various libraries
%_PY_EXE% -m pip install --upgrade pip
%_PIP_EXE% install mysql-python
%_PIP_EXE% install PyMySQL
%_PIP_EXE% install python-dateutil
%_PIP_EXE% install %PY_BS%
%PY_EXE% -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose

:: Collect price_historical_data from various sources
START "" "%SA_DATA_DIR%\r_quantmod\get_quantmod_data.bat"
START "" "%SA_DATA_DIR%\r_oanda\get_oanda_data.bat"
