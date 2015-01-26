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

import urllib3
import datetime
import json



import math

def ToSI(d):
  incPrefixes = ['k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
  decPrefixes = ['m', 'µ', 'n', 'p', 'f', 'a', 'z', 'y']

  degree = int(math.floor(math.log10(math.fabs(d)) / 3))

  prefix = ''

  if degree!=0:
    ds = degree/math.fabs(degree)
    if ds == 1:
      if degree - 1 < len(incPrefixes):
        prefix = incPrefixes[degree - 1]
      else:
        prefix = incPrefixes[-1]
        degree = len(incPrefixes)

    elif ds == -1:
      if -degree - 1 < len(decPrefixes):
        prefix = decPrefixes[-degree - 1]
      else:
        prefix = decPrefixes[-1]
        degree = -len(decPrefixes)

    scaled = float(d * math.pow(1000, -degree))
    
    s = "{scaled} {prefix}".format(scaled=scaled, prefix=prefix)

  else:
    s = "{d} ".format(d=d)

  return(s)

class MiningCalculator:
    def __init__(self):
        pass
    
    def update(self):
        self.update_data()
        self.print_msg()
        self.write_flat_db()

    def print_msg(self):
        msg = """
======= {dt} =======
{cur1} mining calculator
=====================
Hash rate: {hash_rate_hash_per_s}hash/s
Power consumption: {power_consumption_W} W
Hardware price: {hardware_price} {cur2}
Current difficulty: {current_difficulty}
Reward for finding a block: {block_reward_cur1} {cur1}
You will make {revenue_cur1_per_day:0.10f} {cur1} in the next 24 hours at this rate
System efficiency:
  {system_efficiency_hash_per_J}hash/s/W (hash/J)
  {system_efficiency_hash_per_second_per_currency}hash/s/$
Conversion rate (pair {cur1}{cur2}): {conversion_rate_cur1cur2} {cur2} for 1 {cur1}
Electricity rate: {electricity_rate_currency_per_kWh} {cur2}/kWh
Power cost: {power_cost_per_day} {cur2}/day
Revenue: {revenue_per_day} {cur2}/day
Revenue (less power cost): {revenue_less_power_costs_per_day} {cur2}/day
Hardware break even: {hardware_break_even}
Average generation time for a block (solo): {average_generation_time_for_a_block_solo}
Timeframe: {timeframe_months} month(s)
Power cost: {power_cost_per_timeframe:0.2f} {cur2} for {timeframe_months} month(s)
Revenue: {revenue_per_timeframe:0.2f} {cur2} for {timeframe_months} month(s)
Revenue (less power cost): {revenue_less_power_costs_per_timeframe:0.2f} {cur2} for {timeframe_months} month(s)
""".format(
   dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
   hash_rate_hash_per_s = ToSI(self.hash_rate_hash_per_s),
   power_consumption_W = self.power_consumption_W,
   hardware_price = self.hardware_price,
   cur1 = self.cur1,
   cur2 = self.cur2,
   current_difficulty = self.current_difficulty,
   block_reward_cur1 = self.block_reward_cur1,
   revenue_cur1_per_day = self.revenue_cur1_per_day,
   conversion_rate_cur1cur2 = self.conversion_rate_cur1cur2,
   electricity_rate_currency_per_kWh = self.electricity_rate_currency_per_kWh,
   power_cost_per_day = self.power_cost_per_day,
   revenue_per_day = self.revenue_per_day,
   revenue_less_power_costs_per_day = self.revenue_less_power_costs_per_day,
   system_efficiency_hash_per_J = ToSI(self.system_efficiency_hash_per_J),
   system_efficiency_hash_per_second_per_currency = ToSI(self.system_efficiency_hash_per_second_per_currency),
   hardware_break_even = self.hardware_break_even,
   average_generation_time_for_a_block_solo = self.average_generation_time_for_a_block_solo,
   timeframe_months = self.timeframe_months,
   power_cost_per_timeframe = self.power_cost_per_timeframe,
   revenue_per_timeframe = self.revenue_per_timeframe,
   revenue_less_power_costs_per_timeframe = self.revenue_less_power_costs_per_timeframe
   #revenue_less_power_costs_per_timeframe = locale.format("%f", self.revenue_less_power_costs_per_timeframe, grouping=True)
   )

        print(msg)

    def write_flat_db(self):
        with open("flatDB_{cur1}{cur2}.txt".format(cur1=self.cur1, cur2=self.cur2), "a") as myfile:
            myfile.write("{dt} {hash_rate_hash_per_s} {block_reward_cur1} {current_difficulty} {revenue_cur1_per_day:0.10f} {power_cost_per_day} {revenue_per_day} {revenue_less_power_costs_per_day}\n".format(
                dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                hash_rate_hash_per_s = self.hash_rate_hash_per_s,
                block_reward_cur1 = self.block_reward_cur1,
                current_difficulty = self.current_difficulty,
                revenue_cur1_per_day = self.revenue_cur1_per_day,
                power_cost_per_day = self.power_cost_per_day,
                revenue_per_day = self.revenue_per_day,
                revenue_less_power_costs_per_day = self.revenue_less_power_costs_per_day
                ))

    def get_json(self):
        return(json.dumps(self.__dict__))
        # ToFix TypeError: datetime.timedelta(6, 71762, 590987) is not JSON serializable
        # use Simplejson ?
