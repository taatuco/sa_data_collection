# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from ta_main_update_data import *

def recalc_histdata(symbol):
    try:
        get_update_instr_data(1,True,symbol)
    except Exception as e: print(e)


print("###############################################################################")
print("Recalculate historical data for specific function")
print("-------------------------------------------------")
print("IMPORTANT: BACKUP THE DATABASE PRIOR TO RUN THIS SCRIPT")
print("recalc_histdata(symbol)")
print(" ")
print("provide the following parameters:")
print("(1) symbol")
print("--------------------------------------")
print("Affected tables/column:")
print("-----------------------")
print("1. price_instruments_data.*")
print("###############################################################################")
