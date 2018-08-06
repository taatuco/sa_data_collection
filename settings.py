# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os

class sa_path:
    rdir = os.path.dirname(os.path.realpath(__file__))

    def get_path_pwd(self):
        return "C:\\xampp\\htdocs\\_sa\\sa_pwd"

    def get_path_data(self):
        return self.rdir + "\\ta_data"

    def get_path_ta_data_src(self):
        return self.rdir + "\\ta_data\\src"

    def get_path_JSON_rep(self):
        return "c:\\xampp\\htdocs\\_sa\\_sa_app\\json"
