import krakenex
import time
from datetime import datetime
import ticker as t
k=krakenex.API()
k.load_key('/home/ubuntu/kraken/krakenkey.key')
assetcodes={'ask':'a','bid':'b','lastTrade':'c','volumeToday':'v','volumeWeightedAverage':'p','numberOfTrades':'t','lowestToday':'l','HighestToday':'h','openToday':'o'}
#This strategy will decide whether to buy or not based on volume weighted average. if bid<vwa then buy else sell
def vwadecission(pair,tickerpair):
	if t.getTick(tickerpair,'bid')<t.getTick(tickerpair,'volumeWeightedAverage'):
		return 'Buy Signal'
	else:
		return 'Sell Signal'
def whichCryptoToBuy():
	ticker=t.getTicker(k)
#	print ticker
	for pair,tickerpair in ticker.iteritems():
		print pair
		vwadecission(pair,tickerpair)
#		print t.getTick(tickerpair,'bid')-t.getTick(tickerpair,'volumeWeightedAverage')
#		print t.getTick(tickerpair,'volumeWeightedAverage')
#		print t.getTick(tickerpair,'lowestToday')
#		print t.getTick(tickerpair,'HighestToday')	

#assetcodes={'ask':'a','bid':'b','lastTrade':'c','volumeToday':'v','volumeWeightedAverage':'p','numberOfTrades':'t','lowestToday':'l','HighestToday':'h','openToday':'o'}
def shouldIBuy(pairpassed):
	signal=''
	ticker=t.getTicker(k)
	for pair,tickerpair in ticker.iteritems():
		if pair==pairpassed:
			signal=vwadecission(pair,tickerpair)
			break
	return signal
#while(1==1):
#	print str(datetime.now())
#	whichCryptoToBuy()
#	time.sleep(1000)
