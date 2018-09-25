# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

#####################
symbol <- "BA"
uid <- 214
fdate <- 2001-01-01
qm_src <- "yahoo"
#####################

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

collect_data <- function() {
  ### Define path and other variables
  xf <- paste(rd, "/sa_data_collection/r_quantmod/src/", sep = "")
  dfrom <- fdate
  dataframe <- as.data.frame(getSymbols(symbol, src = qm_src, from = dfrom, env = NULL))
  ### Set columns name
  colnames(dataframe)[1] <- "open"
  colnames(dataframe)[2] <- "high"
  colnames(dataframe)[3] <- "low"
  colnames(dataframe)[4] <- "close"
  colnames(dataframe)[5] <- "volume"
  colnames(dataframe)[6] <- "adjusted"

  ### Export content to CSV ###
  fn <- paste(uid,".csv", sep = "")
  f <- paste(xf,fn, sep = "")
  print(f)
  write.csv(dataframe, file = f)
}



inst_ini_package()
collect_data()
