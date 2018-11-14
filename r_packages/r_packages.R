
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

inst_ini_package <- function(){
  list.of.packages <- c("lubridate","quantmod", "tidyquant", "DBI", "RMySQL","binhf","tseries","forecast")
  new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
  if(length(new.packages)) install.packages(new.packages, repos="http://cran.us.r-project.org")
  library("quantmod")
  library("lubridate")
  library("DBI")
  library("RMySQL")
  library("binhf")
  library("tseries")
  library("forecast")
  install.packages("devtools")
  devtools::install_github("rstudio/rstudioapi")
}
