""" Collect and compute strategy portfolio data """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import os

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = SmartAlphaPath()

sys.path.append(os.path.abspath( sett.get_path_feed() ))
from get_portf_alloc import *
from get_portf_perf import *
from set_portf_feed import *
from rm_portf_underpf import *
from pathlib import Path

rm_portf_underpf(250)
get_portf_alloc()
get_portf_perf()
set_portf_feed()
