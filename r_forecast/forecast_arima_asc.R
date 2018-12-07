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

source(paste(rd,"/sa_data_collection/r_packages/r_packages.R", sep = "") )

forecast_data <- function() {

  source(paste(rd,"/sa_pwd/sa_access.R", sep = "") )

  xf <- paste(rd, "/sa_data_collection/src/", sep = "" )
  csvf <- paste(rd, "/sa_data_collection/r_quantmod/src/", sep = "")
  startYear <- year(now()-1)
  startMonth <- 01
  startDay <- 01
  StartDate <- paste(startYear,startMonth,startDay,sep = "-")
  forecastNumbOfdays <- 7

  db_usr <- get_sa_usr()
  db_pwd <- get_sa_pwd()

    m = dbDriver("MySQL")
  myHost <- get_sa_db_srv()
  myDbname <- get_sa_db_name()
  myPort <- 3306
  con <- dbConnect(m, user= db_usr, host= myHost, password= db_pwd, dbname= myDbname, port= myPort)

  sql <- "SELECT symbol, uid FROM symbol_list"
  res <- dbSendQuery(con, sql)

  symbol_list <- fetch(res, n = -1)
  i <- 1
  while (i <= (nrow(symbol_list)/2)+1 ) {
    tryCatch({
      symbol <- symbol_list[i,1]
      uid <- symbol_list[i,2]
      hd_sql <- paste("SELECT date, price_close FROM price_instruments_data WHERE symbol ='",symbol,"' AND date>=",StartDate," ORDER BY date ASC", sep = "")
      hd_res <- dbSendQuery(con, hd_sql)
      mydata <- fetch(hd_res, n = -1)

        attach(mydata)
        T <- mydata
        price <- ts(T$price_close)
        ts_price <- ts(price)

        tryCatch({
          fit <- arima(ts_price,order = c(9,0,10))
          fc  <- forecast(fit, h = forecastNumbOfdays)
          fn <- paste(uid,"f.csv", sep = "")
          f <- paste(xf,fn, sep = "")
          write.csv(fc, file = f)
        },
          error=function(e){
            tryCatch({
              cat("ERROR :",conditionMessage(e), "\n")
              fit <- arima(ts_price,order = c(9,1,10))
              fc  <- forecast(fit, h = forecastNumbOfdays)
              fn <- paste(uid,"f.csv", sep = "")
              f <- paste(xf,fn, sep = "")
              write.csv(fc, file = f)
            }, error=function(e){
              print(symbol)
              cat("ERROR :",conditionMessage(e), "\n")
              fit <- auto.arima(ts_price, stepwise = F, approximation = F)
              fc  <- forecast(fit, h = forecastNumbOfdays)
              fn <- paste(uid,"f.csv", sep = "")
              f <- paste(xf,fn, sep = "")
              write.csv(fc, file = f)
            })
          })
      }, error=function(e){
        cat("ERROR :",conditionMessage(e), "\n")
      })
      i = i+1
  }

}



inst_ini_package()
forecast_data()
