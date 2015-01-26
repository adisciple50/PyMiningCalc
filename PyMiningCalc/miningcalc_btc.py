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

from MiningCalc.miningcalc import *
from MiningCalc.calc import *


class BTCMiningCalculator(MiningCalculator):
    def update_data(self):
        self.hash_rate_hash_per_s = 90.0E9 # hash/s
        """
        BitForce Jalapeno : 4.5 Ghash/s
        BitForce 'Little' Single SC : 30 Ghash/s
        BitForce Single 'SC' : 60 Ghash/s
        BitForce Mini Rig 'SC' : 1'500 Ghash/s
        """
    
        """
        Electrical power, energy and cost
        """
        #self.electricity_rate_currency_per_kWh = 0.14269 # counter_currency per kWh # 0.15 USD/kWh # 0.12EUR/kWh
        self.electricity_rate_currency_per_kWh = (0.0935*8.0 + 0.0578*16.0)/24.0 # HC de 21h45 à 5h45 ; HP=0.0935 HC=0.0578 avg=0.0697 @ 2012-10-22
        # http://www.energy.eu/#Domestic
    
        self.power_consumption_W = 90.0 # W
    
        self.hardware_price = 649.0 + 88.0 + 1299.0 + 88.0
    
    
        """
        Conversion rate currency / BTC
        """
        self.cur1 = 'BTC' # base currency
        self.cur2 = 'USD' # quote currency or counter currency
        #self.pair = "{0}{1}".format(self.cur1, self.cur2) # BTCEUR BTCUSD
        #url = "https://mtgox.com/api/1/{pair}/ticker".format(pair=self.pair)
        url = "http://api.bitcoincharts.com/v1/weighted_prices.json"
        json_data = bytes(urllib3.connection_from_url(url).urlopen("GET", url).data).decode()
        print(json_data)
        Json_weighted = json.loads(json_data)
        #self.conversion_rate_cur1cur2 = float(data['return']['avg']['value'])
        self.conversion_rate_cur1cur2 = float(Json_weighted[self.cur2]['24h'])


        #conversion_rate_cur1cur2 = 22.79 #counter_currency per base_currency
        #self.conversion_rate_cur1cur2 = 1.0 # cur2 for 1 cur1


        """
        block_reward_cur1 and current_difficulty
        """
        self.block_reward_cur1 = float(bytes(urllib3.connection_from_url('http://blockexplorer.com/q/bcperblock').urlopen("GET",'http://blockexplorer.com/q/bcperblock').data).decode())
        self.current_difficulty = float(bytes(urllib3.connection_from_url('http://blockexplorer.com/q/bcperblock').urlopen("GET",'http://blockexplorer.com/q/getdifficulty').data).decode())

        self.revenue_cur1_per_day = float(self.hash_rate_hash_per_s)*self.block_reward_cur1/self.current_difficulty*(60.0*60*24*(2**16-1)/(2**48))
        # maybe I should use arbitrary precision (libs such as decimal or mpmath)

        self.power_cost_per_day = float(self.power_consumption_W)*24.0*self.electricity_rate_currency_per_kWh/1000.0
        self.revenue_per_day = self.revenue_cur1_per_day*self.conversion_rate_cur1cur2
        self.revenue_less_power_costs_per_day = self.revenue_per_day - self.power_cost_per_day
    
        self.hardware_break_even = datetime.timedelta(days=float(self.hardware_price)/float(self.revenue_less_power_costs_per_day))

        self.system_efficiency_hash_per_J = float(self.hash_rate_hash_per_s)/float(self.power_consumption_W) # hash/J or hash/s/W
        self.system_efficiency_hash_per_second_per_currency = float(self.hash_rate_hash_per_s)/float(self.hardware_price)
    
    
        """
        Timeframe calculator
        """
        self.timeframe_months = 1 # months
        days_per_months = 365.0/12.0
        self.power_cost_per_timeframe = self.power_cost_per_day * self.timeframe_months * days_per_months
        self.revenue_per_timeframe = self.revenue_per_day * self.timeframe_months * days_per_months
        self.revenue_less_power_costs_per_timeframe = self.revenue_less_power_costs_per_day * self.timeframe_months * days_per_months
    
    
        self.average_generation_time_for_a_block_solo = datetime.timedelta(days=self.block_reward_cur1/self.revenue_cur1_per_day)

if __name__ == '__main__':
    test = BTCMiningCalculator()
    test.update_data()
    print(test.current_difficulty)