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
source(paste(rd, "/sa_data_collection/r_packages/r_packages.R", sep = "") )

get_date_prev_month <- function(yyyy,mm,dd) {
  yx <- yyyy
  mx <- mm
  dx <- dd

  if (mx == 1) {
    mx <- 12
    yx <- yx -1
  } else {
    mx <- mx -1
    if (mx < 10) {
      mx <- paste("0",mx, sep = "")
    }
  }

  date_yyyymmdd <- paste(yx,mx,dx, sep = "-")
  return(date_yyyymmdd)

}

collect_data <- function() {
  ### Define path and other variables
  source(paste(rd, "/sa_pwd/sa_access.R", sep = "")  )
  xf <- paste(rd, "/sa_data_collection/r_quantmod/src/", sep = "")
  qm_src <- "yahoo"
  yx <- year(now())
  mx <- month(now())
  dfrom <- get_date_prev_month(yx,mx,"01")

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
      tryCatch({
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
      }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
      i = i+1
    }
  }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})

}



inst_ini_package()
collect_data()
