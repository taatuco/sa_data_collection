# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def get_pct_change(ini_val,new_val):

    if not new_val == 0:
        r = (new_val - ini_val) / new_val
    else:
        r = 0

    return r
