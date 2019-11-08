""" Settings and customization """
# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os

class SmartAlphaPath:
    """
    Get path to program folders.
    Args:
        None
    """
    rdir = os.path.dirname(os.path.realpath(__file__))
    pdir = os.path.abspath(os.path.join(rdir, os.pardir))

    def get_path_pwd(self):
        """ Get password directory """
        return self.pdir+ "\\sa_pwd"

    def get_path_src(self):
        """ Get data source directory """
        return self.rdir+"\\src\\"

    def get_path_labels(self):
        """ Get labels directory """
        return self.rdir + "\\labels"

    def get_path_feed(self):
        """ Get feed directory """
        return self.rdir + "\\feed"

    def get_path_core(self):
        """ Get core directory """
        return self.rdir + "\\core"

    def get_path_portfolios(self):
        """ Get portfolios directory """
        return self.rdir + "\\portfolios"

    def get_path_r_quantmod_src(self):
        """ Get quantmod directory """
        return self.rdir + "\\r_quantmod\\src\\"

    def get_path_r_oanda_src(self):
        """ Get Oanda directory """
        return self.rdir + "\\r_oanda\\src\\"

def debug(txt):
    """
    Print text to the terminal if variable enable_debug is set to True.
    Args:
        txt (string): text to print
    Returns:
        Boolean: return True if debug is enabled.
    """
    enable_debug = False
    if enable_debug:
        print(str(txt))
    return enable_debug

def get_portf_suffix():
    """
    Get the strategy portfolio suffix that differentiate portfolio from
    other financial instruments.
    Args:
        None
    Returns:
        String: Strategy portfolio suffix.
    """
    return "PRF:"

def get_product_name():
    """
    Get product name for this programme
    Args:
        None
    Returns:
        String: Name of product
    """
    return "SmartAlpha"

def get_reply_to_email(what):
    """
    Get information related to email sender such as email address,
    display name, or an alternative address.
    Args:
        None
    Returns:
        String: email address, display name, alternative email.
    """
    ret = ''
    if what == 'email':
        ret = 'no-reply@taatu.co'
    if what == 'name':
        ret = 'SmartAlpha Intelligence'
    if what == 'tech':
        ret = 'tech@taatu.co'
    return ret

def get_email_txt_signature():
    """
    Get email signature.
    Args:
        None
    Returns:
        String: Email signature.
    """
    ret = '\n'+\
    'SmartAlpha Team'+\
    '\n'+\
    'Taatu Ltd.'+\
    '\n'+\
    '27 Old Gloucester Street, London, WC1N 3AX, UK'+\
    '\n'
    return ret
