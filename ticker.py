import time
from datetime import datetime
#Gets ticker result of particular asset. also gets tick e.g if you want ask for 'xxbtzeur'
currpairlist=['XXBTZEUR','XETHZEUR','XXMRZEUR','XETCZEUR','XLTCZEUR','XREPZEUR','XXRPZEUR']
#assetcodes={'ask':'a','bid':'b'}
assetcodes={'ask':'a','bid':'b','lastTrade':'c','volumeToday':'v','volumeWeightedAverage':'p','numberOfTrades':'t','lowestToday':'l','HighestToday':'h','openToday':'o'}

def getTick(pairticker,tick):
	return float(pairticker[assetcodes[tick]][0])
#Returns dict of ticker information of all pairs mentioned in currpairlist
def getTicker(k):
	while (1==1):
		commadelimitedcurrpair= ",".join(currpairlist)

                try:
                        ticker= k.query_public('Ticker',{'pair':commadelimitedcurrpair})
			ticker=ticker['result']
			return ticker
                except Exception as e:
                        print "An Error occured while fetching ticker information" ,str(e)
                        time.sleep(5)
			continue

def printTicks(ticker,assetcode):
	print assetcode,"%.4f" %getTick(ticker,assetcode),
def getPairTicker(k,pair):
	ticker=getTicker(k)
	return ticker[pair]
#Runs ticker continuosly only for one pair
def runPairTicker(k,pair):
	while(1==1):
		ticker=getPairTicker(k,pair)
		printTicks(ticker)
		time.sleep(10)
#Runs ticker continously and prints information as mentioned in assetcodes
def runTicker(k):
	for pair in currpairlist:
                print pair,':',
	print ''
	while(1==1):
		ticker=getTicker(k)
		for tick,assetcode in assetcodes.iteritems():
			for pair in currpairlist:
				printTicks(ticker[pair],tick),
			print ' '
		time.sleep(10)
			
			
		
