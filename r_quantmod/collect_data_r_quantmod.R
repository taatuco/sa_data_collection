
### Install necessary packages
inst_ini_package <- function(){
  list.of.packages <- c("lubridate","quantmod", "tidyquant", "DBI", "RMySQL")
  new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
  if(length(new.packages)) install.packages(new.packages)
  library("quantmod")
  library("lubridate")
  library("DBI")
  library("RMySQL")  
}



collect_data <- function() {

  ### Define path and other variables
  xf <- "C:\\xampp\\htdocs\\_sa\\sa_data_collection\\r_quantmod\\src\\"
  qm_src <- "yahoo"
  yx <- year(now())
  dfrom <- paste(yx,"-01-01",sep = "")

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
      dataframe <- as.data.frame(getSymbols(symbol, src = qm_src, from = dfrom, env = NULL))

      ### Set columns name
      colnames(dataframe)[1] <- "open"
      colnames(dataframe)[2] <- "high"
      colnames(dataframe)[3] <- "low"
      colnames(dataframe)[4] <- "close"
      colnames(dataframe)[5] <- "volume"
      colnames(dataframe)[6] <- "adjusted"

      ### Export content to CSV ###
      fn <- paste(symbol,".csv", sep = "")
      f <- paste(xf,fn, sep = "")
      write.csv(dataframe, file = f)
      i = i+1
    }
  }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})

}



inst_ini_package()
collect_data()
