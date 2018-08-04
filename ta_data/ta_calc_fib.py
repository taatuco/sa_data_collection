# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import sys
import os
import time

pdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(pdir) )
from settings import *
sett = sa_path()

sys.path.append(os.path.abspath( sett.get_path_pwd() ))
from sa_access import *
access_obj = sa_db_access()

db_usr = access_obj.username()
db_pwd = access_obj.password()
db_name = access_obj.db_name()
db_srv = access_obj.db_server()

#Draw lines from today - 20 days

#Fib 0%
#If (day-180-ago) < today: Fib0 = Large(day-180-ago:today)
#else: Fib0 = Small(day-180-ago:today)

#Fib 23.6%
#If (Fib0 < Fib100): Fib0+(Fib100-Fib0)*0.236
#else: Fib0-(Fib0-Fib100)*0.236

#Fib 38.2%
#If (Fib0 < Fib100): Fib0+(Fib100-Fib0)*0.382
#else: Fib0-(Fib0-Fib100)*0.382

#Fib 61.8%
#If (Fib0 < Fib100): Fib0+(Fib100-Fib0)*0.618
#else: Fib0-(Fib0-Fib100)*0.618

#Fib 76.4%
#If (Fib0 < Fib100): Fib0+(Fib100-Fib0)*0.764
#else: Fib0-(Fib0-Fib100)*0.764

#Fib 100%
#If (day-180-ago) < today: Fib100 = Small(day-180-ago:today)
#else: Fib100 = Large(day-180-ago:today)
