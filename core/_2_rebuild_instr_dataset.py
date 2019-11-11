""" Second step of rebuilding data: update and insert new records """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from ta_main_update_data import get_update_instr_data



################################################################################
# Rebuild the data (need to be run twice)
################################################################################
get_update_instr_data(1, False, '')
