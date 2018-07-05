


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