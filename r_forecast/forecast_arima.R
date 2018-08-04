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
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

library(base)
library(rstudioapi)

get_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file <- "--file="
  rstudio <- "RStudio"

  match <- grep(rstudio, args)
  if (length(match) > 0) {
    return(dirname(rstudioapi::getSourceEditorContext()$path))
  } else {
    match <- grep(file, args)
    if (length(match) > 0) {
      return(dirname(normalizePath(sub(file, "", args[match]))))
    } else {
      return(dirname(normalizePath(sys.frames()[[1]]$ofile)))
    }
  }
}

setwd(get_dir() )
setwd("../../")
rd <- getwd()

### Install necessary packages
source(paste(rd,"/sa_data_collection/r_packages/r_packages.R", sep = "") )

forecast_data <- function() {

  ### Define path and other variables
  source(paste(rd,"/sa_pwd/sa_access.R", sep = "") )

  xf <- paste(rd, "/sa_data_collection/r_forecast/src/", sep = "" )
  csvf <- paste(rd, "/sa_data_collection/r_quantmod/src/", sep = "")
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
