DEL /F /Q "C:\xampp\htdocs\_sa\sa_data_collection\r_quantmod\src\*"
"C:\Program Files\R\R-3.5.0\bin\x64\Rscript.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_quantmod\collect_data_r_quantmod.R"

DEL /F /Q "C:\xampp\htdocs\_sa\sa_data_collection\r_forecast\src\*"
"C:\Program Files\R\R-3.5.0\bin\x64\Rscript.exe" "C:\xampp\htdocs\_sa\sa_data_collection\r_forecast\forecast_arima.R"