__author__ = 'Jason'

from MiningCalc.miningcalc_ltc import LTCMiningCalculator
import urllib3
import certifi
import json

class POTMiningCalculator(LTCMiningCalculator):
    def __init__(self):
        self.KilohashASecond = 32000
        self.hash_rate_hash_per_s = self.KilohashASecond * 1000
        self.electricity_rate_currency_per_kWh = 0.23 # counter_currency per kWh # 0.23 USD/kWh
        self.power_consumption_W = 100.0 # W
        self.hardware_price = 2000 # USD
        ### internet data sources that will need to be changed ...
        self.cur1 = 'POT' # base currency
        self.cur2 = 'USD' # quote currency or counter currency - usually usd

        self.blockcount = int(bytes(urllib3.connection_from_url('http://chainz.cryptoid.info/ric/api.dws?q=getblockcount').urlopen("GET", 'http://chainz.cryptoid.info/ric/api.dws?q=getblockcount').data).decode()) #supply an int here.

        ## a breif break form simplicity whilst i plumb in the new data sources

        # http://explorer.potcoin.net/chain/Potcoin/q/getblockcount
        # https://chainz.cryptoid.info/api.dws?q=getblockcount
        url = "https://bleutrade.com/api/v2/public/getticker?market=%s_%s"% (self.cur1, self.cur2)
        #print(url)
        data = bytes(urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where()).urlopen("GET", url).data).decode()
        data = json.loads(data)
        self.conversion_rate_cur1cur2 = float(data['result'][0]['Ask'])

        # "https://bleutrade.com/api/v2/public/getticker?market=%s_%s"%(self.cur1, self.cur2)
    def update_data(self):
        self.current_difficulty = float(bytes(urllib3.connection_from_url('http://chainz.cryptoid.info/pot/api.dws?q=getdifficulty').urlopen("GET", 'http://chainz.cryptoid.info/pot/api.dws?q=getdifficulty').data).decode())

if __name__ == '__main__':
    test = POTMiningCalculator()
    test.update_data()
    print(test.current_difficulty)