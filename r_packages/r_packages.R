
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

inst_ini_package <- function(){
  tryCatch(
    {
      list.of.packages <- c("lubridate","quantmod", "tidyquant", "DBI", "RMySQL","binhf","tseries","forecast")
      new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
      repository <- "http://cran.us.r-project.org"
      if(length(new.packages)) install.packages(new.packages, repos=repository)
      library("quantmod")
      library("lubridate")
      library("DBI")
      library("RMySQL")
      library("binhf")
      library("tseries")
      library("forecast")
      install.packages("devtools", repos=repository)
      devtools::install_github("rstudio/rstudioapi")
    }, error=function(e){
        cat("ERROR :",conditionMessage(e), "\n")
      }
  )
}
