
SET R_VER=R-3.5.0
SET PY_VER=Python36-32

SET SA_DATA_DIR=C:\xampp\htdocs\_sa\sa_data_collection
SET _R_SCRIPT_EXE="C:\Program Files\R\%R_VER%\bin\x64\Rscript.exe"
SET _PY_EXE="%LOCALAPPDATA%\Programs\Python\%PY_VER%\python.exe"

:: Compute forecast points
DEL /F /Q "%SA_DATA_DIR%\r_forecast\src\*"
START "" %_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_forecast\forecast_arima_asc.R"
%_R_SCRIPT_EXE% "%SA_DATA_DIR%\r_forecast\forecast_arima_dsc.R"
