# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os

class sa_path:
    rdir = os.path.dirname(os.path.realpath(__file__))
    pdir = os.path.abspath(os.path.join(rdir, os.pardir))

    def get_path_pwd(self):
        return self.pdir+ "\\sa_pwd"

    def get_path_src(self):
        return self.rdir+"\\api\\src\\"

    def get_path_feed(self):
        return self.rdir + "\\feed"


    def get_path_signals(self):
        return self.rdir + "\\w_signals"

    def get_path_r_quantmod_src(self):
        return self.rdir + "\\r_quantmod\\src\\"

    def get_path_r_oanda_src(self):
        return self.rdir + "\\r_oanda\\src\\"
