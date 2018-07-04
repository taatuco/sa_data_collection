################################################################################
# Desc: Collect historical data using quantmod library (source yahoo finance)
#
# Connect to MySQL database to retrieve the list of symbols to fetch for data.
# Locate data and export content to csv files.
#
# inst_ini_package() = Check if all the necessary packages are installed.
# collect_data() = Retrieve symbols from database and output results in csv.
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
