""" Collect instrument data, send intel report and collect news """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import datetime
from send_intel_report_email import send_intel_report

TODAY_DATE = datetime.datetime.now()
TODAY_DAY_OF_WEEK = TODAY_DATE.weekday()

SATURDAY_ID = 5
SUNDAY_ID = 6

if TODAY_DAY_OF_WEEK != 5 and TODAY_DAY_OF_WEEK != 6:
    send_intel_report()
