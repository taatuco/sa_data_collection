:: Batch: data collection

SET R_VER=R-3.5.0
SET PY_VER=Python36-32
SET PY_BS=beautifulsoup4

SET SA_DATA_DIR=C:\xampp\htdocs\_sa\sa_data_collection
SET LOGFILE="%SA_DATA_DIR%\sa_col_log.log"
SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PIP_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\Scripts\pip.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"


%_PY_EXE% "%SA_DATA_DIR%\data\ta_main_update_data.py"
