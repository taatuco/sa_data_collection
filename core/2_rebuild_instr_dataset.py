# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
from pathlib import Path
from ta_main_update_data import *



################################################################################
# Rebuild the data (need to be run twice)
################################################################################
get_update_instr_data(1,False,'')
