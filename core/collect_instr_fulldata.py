# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from ta_main_update_data import *
from send_intel_report_email import *
from get_newsdata import *
get_update_instr_data(1,False,'')
send_intel_report()
get_newsdata(1,True)
