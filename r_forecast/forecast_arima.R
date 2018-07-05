################################################################################
# Desc: ARIMA with an autofit forcast
#
# Collect the historical data from csv files and output forecast point
# using ARIMA autofit.
#
# inst_ini_package() = Check if all the necessary packages are installed.
# forecast_data() = Run the forecast of various csv files and ouput results in csv.
#
# Auth: dh@taatu.co (Taatu Ltd.)
# Date: July 1, 2018
################################################################################

# Licensed under The MIT License
# Copyright 2018 Taatu Ltd. 27 Old Gloucester Street, London, WC1N 3AX, UK (http://taatu.co)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


### Install necessary packages
inst_ini_package <- function(){
  list.of.packages <- c("lubridate","quantmod", "tidyquant", "DBI", "RMySQL","binhf","tseries","forecast")
  new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
  if(length(new.packages)) install.packages(new.packages)
  library("quantmod")
  library("lubridate")
  library("DBI")
  library("RMySQL")
  library("binhf")
  library("tseries")
  library("forecast")
}

forecast_data <- function() {

  ### Define path and other variables
  source("C:\\xampp\\htdocs\\_sa\\sa_pwd\\sa_access.R")
  xf <- "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_forecast\\src\\"
  csvf <- "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_quantmod\\src\\"
  qm_src <- "yahoo"
  startYear <- year(now()-1)
  startMonth <- 01
  startDay <- 01
  StartDate <- paste(startYear,startMonth,startDay,sep = "-")
  forecastNumbOfdays <- 7

  ### Connect to MySQL database to retrieve list of symbols
  db_usr <- get_sa_usr()
  db_pwd <- get_sa_pwd()
  # create a driver
  m = dbDriver("MySQL")
  myHost <- get_sa_db_srv()
  myDbname <- get_sa_db_name()
  myPort <- 3306
  con <- dbConnect(m, user= db_usr, host= myHost, password= db_pwd, dbname= myDbname, port= myPort)

  sql <- "SELECT * FROM symbol_list"
  res <- dbSendQuery(con, sql)

  tryCatch({
    symbol_list <- fetch(res, n = -1)
    i <- 1
    while (i < nrow(symbol_list)) {
      ### Define data to collect
      symbol <- symbol_list[i,5]
      csvFile <- paste(csvf,symbol,".csv",sep = "")
      if(file.exists(csvFile)){
        mydata<- as.data.frame(read.csv(file = csvFile,header = TRUE, sep = ","))

        attach(mydata)
        T <- mydata
        price <- ts(T$close)
        ts_price <- ts(price, start = c(startYear, startMonth), frequency = nrow(T))
        fit <- auto.arima(ts_price, stepwise = F, approximation = F)
        fc  <- forecast(fit, h = forecastNumbOfdays, level = c(75, 85, 95))
        dataframe <- as.data.frame(fc)

        ### Export forecast to CSV ###
        fn <- paste(symbol,".csv", sep = "")
        f <- paste(xf,fn, sep = "")
        write.csv(dataframe, file = f)
     }
        i = i+1
    }
  }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})

}



inst_ini_package()
forecast_data()
