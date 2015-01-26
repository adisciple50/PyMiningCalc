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
import certifi #uses certs from firefox compatable browsers.chromium/google-chrome ssl certificates should also work without modification.

class LTCMiningCalculator(MiningCalculator):
    def reward(self, blocknumber):
        return 50.0 / (2 ** int((blocknumber + 1) / 840000))
        # initial reward is 50 LTC
        # reward is halfed every 840'000 blocks

    def update_data(self):
        """https://github.com/litecoin-project/litecoin/wiki/Mining-hardware-comparison"""
        self.hash_rate_hash_per_s = 600.0E3 # hash/s

        """
        Electrical power, energy and cost
        """
        #self.electricity_rate_currency_per_kWh = 0.14269 # counter_currency per kWh # 0.15 USD/kWh # 0.12EUR/kWh
        self.electricity_rate_currency_per_kWh = (0.0935*8.0 + 0.0578*16.0)/24.0 # HC de 21h45 à 5h45 ; HP=0.0935 HC=0.0578 avg=0.0697 @ 2012-10-22
        # http://www.energy.eu/#Domestic

        self.power_consumption_W = 500.0 # W

        self.hardware_price = 2000


        """
        Conversion rate currency / BTC
        """
        self.cur1 = 'LTC' # base currency
        self.cur2 = 'USD' # quote currency or counter currency
        self.pair = "{0}{1}".format(self.cur1, self.cur2) # BTCEUR BTCUSD
        url = "https://btc-e.com/api/2/{cur1}_{cur2}/ticker".format(cur1=self.cur1.lower(), cur2=self.cur2.lower())
        json_data = bytes(urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where()).urlopen("GET", url).data).decode()
        data = json.loads(json_data)
        self.conversion_rate_cur1cur2 = float(data['ticker']['sell'])
        #self.conversion_rate_cur1cur2 = 1.25 # ToFix cur2 for 1 cur1 #counter_currency per base_currency


        """
        block_reward_cur1 and current_difficulty
        """
        #self.block_reward_cur1 = float(urllib2.urlopen('https://blockexplorer.com/q/bcperblock').read())
        #self.current_difficulty = float(urllib2.urlopen('http://blockexplorer.com/q/getdifficulty').read())
        #self.current_difficulty = float(urllib2.urlopen('http://abe.john-edwin-tobey.org/chain/Bitcoin/q/getdifficulty').read())
        #self.current_difficulty = float(urllib2.urlopen('http://abe.john-edwin-tobey.org/chain/Bitcoin/q/getdifficulty').read())

        #self.block_reward_cur1 = 50 # ToFix
        #blockcount = int(urllib2.urlopen('http://explorer.litecoin.net/chain/Litecoin/q/getblockcount').read())
        self.blockcount = int(bytes(urllib3.connection_from_url('http://explorer.litecoin.net/chain/Litecoin/q/getblockcount').urlopen("GET", 'http://explorer.litecoin.net/chain/Litecoin/q/getblockcount').data).decode())
        self.block_reward_cur1 = self.reward(self.blockcount)

        #self.current_difficulty = 96.19595881 #ToFix
        """self.data = ...blockNumber:          height of last block in interval + 1
time:                 block time in seconds since 0h00 1 Jan 1970 UTC
target:               decimal target at blockNumber
avgTargetSinceLast:   harmonic mean of target over interval
difficulty:           difficulty at blockNumber
hashesToWin:          expected number of hashes needed to solve a block at this difficulty
avgIntervalSinceLast: interval seconds divided by blocks
netHashPerSecond:     estimated network hash rate over interval

Statistical values are approximate and differ slightly from http://blockexplorer.com/q/nethash.

/chain/CHAIN/q/nethash[/INTERVAL[/START[/STOP]]]
Default INTERVAL=144, START=0, STOP=infinity.
Negative values back from the last block.

blockNumber,time,target,avgTargetSinceLast,difficulty,hashesToWin,avgIntervalSinceLast,netHashPerSecond
START DATA
329075,1365277569,131013658748435477164936169388574986983635210083111099862121185280,131013658748436269891309801177314810748808714944246301785889148798,205.779,883816926750,228,3876390030
"""
        # self.data = urllib2.urlopen('http://explorer.litecoin.net/chain/Litecoin/q/nethash/1/-3').read() # old urllib2 line.
        self.data = bytes(urllib3.connection_from_url('http://explorer.litecoin.net/chain/Litecoin/q/nethash/1/-3').urlopen("GET", 'http://explorer.litecoin.net/chain/Litecoin/q/nethash/1/-3').data).decode()

        self.data = self.data.split('\n')
        self.data = self.data[len(self.data)-2]
        self.data = self.data.split(',')
        self.current_difficulty = float(self.data[4])

        self.revenue_cur1_per_day = float(self.hash_rate_hash_per_s)*self.block_reward_cur1/(self.current_difficulty*(2**16-1)*2**16)*60.0*60*24
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
    test = LTCMiningCalculator()
    test.update_data()
    print(test.current_difficulty)