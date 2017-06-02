import requests
import time
import os
from datetime import datetime
#BaseLinkUrl='https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH,LTC,ETC&tsyms=EUR,EUR,EUR,EUR'
exch=['Bitstamp','Coinbase','Quoine','BitMarket','Paymium','BTCE','BitBay','TheRockTrading','Kraken','BitSquare','itBit','Exmo','Coinfloor','Gatecoin']
BaseLinkUrl='https://www.cryptocompare.com/api/data/coinsnapshot/?fsym=BTC&tsym=EUR'
BaseLinkUrl='https://www.cryptocompare.com/api/data/coinsnapshot/?fsym='
oldexchanges=[]
cryptos=['BTC','ETH','ETC','LTC']
while(1==1):
    for crypto in cryptos:
	target = open('coincompare.txt'+crypto, 'a+')
	try:
		r = requests.get(BaseLinkUrl+crypto+'&tsym=EUR')
		r=r.json()
	except Exception as e:
		time.sleep(10)
		continue
	if int(r['Type'])>=100:
		exchanges=r['Data']['Exchanges']
		os.system('clear')
		target.write('\n'+str(datetime.now())+'\t')
		for exchange in exchanges:
			if exchange['MARKET'] in str(exch):
				if len(oldexchanges)==len(exch):
					for oldexch in oldexchanges:
						if oldexch['MARKET']==exchange['MARKET']:
							target.write(exchange['MARKET']+':'+"%.4f" %float(exchange['PRICE'])+'\t')
							print exchange['MARKET'],':',"%.4f" %float(exchange['PRICE'])
				else:
					oldexchanges.append(exchange)
#	print exchanges
	else:
		print "Error"
	target.close()
	time.sleep(15)
