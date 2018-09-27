
SET R_VER=R-3.5.0
SET PY_VER=Python36-32

SET SA_DATA_DIR=C:\xampp\htdocs\_sa\sa_data_collection
SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"

:: Collect price_historical_data from various sources
DEL /F /Q "%SA_DATA_DIR%\r_quantmod\src\*"
%_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_quantmod\collect_data.R"
START "" %_PY_EXE% "%SA_DATA_DIR%\r_quantmod\insert_db_price_data_asc.py"
%_PY_EXE% "%SA_DATA_DIR%\r_quantmod\insert_db_price_data_dsc.py"
