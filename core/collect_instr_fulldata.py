""" Collect instrument data, send intel report and collect news """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from ta_main_update_data import get_update_instr_data
from send_intel_report_email import send_intel_report

get_update_instr_data(0, False, '')
send_intel_report()
