#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    Crypto-currency mining calculator

    Copyright (C) 2013 "Working4coins" <working4coins@gmail.com>
    You can donate: https://sites.google.com/site/working4coins/donate

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import time
import datetime

#import simplejson as json
#import locale

import os
import argparse

from MiningCalc.miningcalc_btc import BTCMiningCalculator
from MiningCalc.miningcalc_ltc import LTCMiningCalculator

if __name__ == "__main__":
    #locale.setlocale(locale.LC_ALL, 'en_US') # to print number with commas as thousands separators
    #locale.setlocale(locale.LC_ALL, 'fr_FR') # to print number with commas as thousands separators

    parser = argparse.ArgumentParser(description='Use the following parameters')
    parser.add_argument('currency1', action="store", help="use this flag to set currency mining calculator (BTC, LTC...)")  
    parser.add_argument('--loop', action="store", help="use this flag to run program in an infinite loop (LOOP parameters is pause in seconds)")
    args = parser.parse_args()
  
    args.basepath = os.path.dirname(__file__)
    
    args.currency1 = args.currency1.upper()
    
    if args.currency1=='BTC':
      calc = BTCMiningCalculator()
    elif args.currency1=='LTC':
      calc = LTCMiningCalculator()
    else:
      calc = None

    if calc!=None:

        if args.loop==None:
            calc.update()
        else:
            delay_s = float(args.loop)
            while True:
                calc.update()
                dt_next = datetime.now() + timedelta(seconds=delay_s)
                print("="*10)
                print("Waiting... next update @ {dt_next}".format(dt_next=dt_next.strftime("%Y-%m-%d %H:%M")))
                time.sleep(delay_s)

    else:
        print("Undefined currency")
