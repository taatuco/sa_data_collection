""" Collect and compute strategy portfolio data """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
PDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(PDIR))
from settings import SmartAlphaPath
SETT = SmartAlphaPath()
sys.path.append(os.path.abspath(SETT.get_path_core()))
from sa_logging import log_this
sys.path.append(os.path.abspath(SETT.get_path_feed()))
from get_portf_alloc import get_portf_alloc
from get_portf_perf import get_portf_perf
from set_portf_feed import set_portf_feed
from rm_portf_underpf import rm_portf_underpf

log_this('4. portf_main_get_data', 0)
rm_portf_underpf(250)
get_portf_alloc()
get_portf_perf()
set_portf_feed()
log_this('4. portf_main_get_data', 0)
