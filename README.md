# PyMiningCalc #

## Python3 Output Calculator for Bitcoin/Litecoin Based Currencies.##


=== Credits and Origin ===

this is just an update of this google code project from ages ago, i couldnt find a matching github repository:

https://code.google.com/p/crypto-mining-calc/

and the project web page is here:

https://sites.google.com/site/working4coins/calculator

the original code wasnt mine, and urllib2 is long dead for python3, and it also had a couple of errors. this project is now shippable.

=== Created By === 

@Working4Coins (twitter)

Updated and posted by:

@deddokatana (twitter)

=== Usage ===

for those familiar with the old library, you will recognise this one.. all the functions return the same thing as they did before, its only the web sources that have been updated, ive also added my own custom use module for an example and modding.

but these are the class properties that will need to be supplied/ modified. (according to the working for coins site above):

in miningcalc_btc.py and miningcalc_ltc.py:

Change

        self.hash_rate_hash_per_s = 60.0E9 # hash/s
        self.electricity_rate_currency_per_kWh = 0.15
        self.power_consumption_W = 100.0 # W
        self.hardware_price = 2000 # USD


and run run_calc.sh on most desktop operating systems, and it should work.

otherwise when writing your own code - Class extending and overiding is demonstrated in miningcalc_pot.py:

    from MiningCalc.miningcalc_btc import BTCMiningCalculator
	from MiningCalc.miningcalc_ltc import LTCMiningCalculator
	
	class MyBtcClass(BTCMiningCalculator):
		def __init__(self):
		self.hash_rate_hash_per_s = 60.0E9 # hash/s
        self.electricity_rate_currency_per_kWh = 0.15
        self.power_consumption_W = 100.0 # W
        self.hardware_price = 2000 # USD
		#further overides and additional methods
	class MyLtcClass(LTCMiningCalculator):
	def __init__(self):
		self.hash_rate_hash_per_s = 60.0E9 # hash/s
        self.electricity_rate_currency_per_kWh = 0.15
        self.power_consumption_W = 100.0 # W
        self.hardware_price = 2000 # USD
		#further overides and additional methods

a setup.py installer is included but untested:

	cd /SetupFolderLocation (please google "cd in a terminal/commandline" for your operating system if neccessary)

then:

	python ./setup.py install 

(or whatever...)


=== Donations ===

the originator crypto currency wallets are:

BTC : 1CZzhk6UkpTNKsJfNAsnKBr9VYYLPfsqaA

LTC : Li7mRwpt5WwXeXzsK3qJLhKjSjUBM1hxov

DVC : 1Nnm9nyacVYxruKfQKzUzHwQWUEi2bCz7v


mine is:
 
POT : PGhrHvk4SAcZQwPfutSjyFnNwSbkJjfAxB - im not doing anything immoral, i just really like the coin! :D

=== Notes ===

miningcalc_ltc.py - will need updating  to json in future. to do this, just change:

self.data = bytes(urllib3.connection_from_url('http://explorer.litecoin.net/chain/Litecoin/q/nethash/1/-3').urlopen("GET", 'http://explorer.litecoin.net/chain/Litecoin/q/nethash/1/-3').data).decode()

to

self.data = bytes(urllib3.connection_from_url('http://explorer.litecoin.net/chain/Litecoin/q/nethash/1/-3').urlopen("GET", 'http://explorer.litecoin.net/chain/Litecoin/q/nethash/1/-3?format=json').data).decode()

and assign the rest of the self.data values. right now it aint broke so i wont fix it.
