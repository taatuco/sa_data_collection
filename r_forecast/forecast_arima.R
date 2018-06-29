
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
  xf <- "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_forecast\\src\\"
  csvf <- "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_quantmod\\src\\"
  qm_src <- "yahoo"
  startYear <- year(now()-1)
  startMonth <- 01
  startDay <- 01
  StartDate <- paste(startYear,startMonth,startDay,sep = "-")
  forecastNumbOfdays <- 7  

  ### Connect to MySQL database to retrieve list of symbols
  db_usr <- "sa_db_user"
  db_pwd <- "9XHWVxTH9ZJnshvN"
  # create a driver
  m = dbDriver("MySQL")
  myHost <- "127.0.0.1"
  myDbname <- "smartalpha"
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
