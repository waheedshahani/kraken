import random
import ticker as t
import krakenex
import time
from datetime import datetime
import decide as d
import percent

k=krakenex.API()
k.load_key('/home/ubuntu/kraken/krakenkey.key')
pripub={'Time':'pub','Assets':'pub','AssetPairs':'pub','Ticker':'pub','OHLC':'pub','Depth':'pub','Trades':'pub','Spread':'pub','Balance':'pri','TradeBalance':'pri','OpenOrders':'pri','ClosedOrders':'pri','QueryOrders':'pri','TradesHistory':'pri','QueryTrades':'pri','OpenPositions':'pri','Ledgers':'pri','QueryLedgers':'pri','TradeVolume':'pri','AddOrder':'pri','CancelOrder':'pri',}

currpair={'btceur':'XXBTZEUR','etheur':'XETHZEUR','xmreur':'XXMRZEUR','etceur':'XETCZEUR','etceth':'XETCXETH','repeur':'XREPZEUR','xlmeur':'XXLMZEUR','xrpeur':'XXRPZEUR','XDGBTC':'XXDGXXBT'}
currpairlist=['XXBTZEUR','XETHZEUR','XXMRZEUR','XETCZEUR','XETCXETH','XREPZEUR','XXLMZEUR','XXRPZEUR','XXDGXXBT']
commadelimitedcurrpair= ",".join(currpairlist)
#dictionary contains crypto and their decimal points so that we put order by increasing decimal points.
deci={'ETH':0.00001,'ETC':0.00001,'LTC':0.00001,'REP':0.00001,'XBT':0.001,'XLM':0.000001,'XRP':0.000001}

pair=''

def QueryOrders(txid):
	try:
		result=k.query_private('QueryOrders',{'txid':txid})['result'][txid]
		fee=float(result['fee'])
		volexec=float(result['vol_exec'])
		return [fee,volexec]	
	except Exception as e:
		print e
		return [0,0]
#	print result
#QueryOrders('OBF4I2-IZNDT-SNXASY')
def chooseCurrPair():
	global pair
	currpair={'btceur':'XXBTZEUR','etheur':'XETHZEUR','xmreur':'XXMRZEUR','ltceur':'XLTCZEUR','etceur':'XETCZEUR','etceth':'XETCXETH','repeur':'XREPZEUR','xlmeur':'XXLMZEUR','xrpeur':'XXRPZEUR','XDGBTC':'XXDGXXBT'}
	currpairlist=[]
	while(1==1):
		i=0
		for key,value in currpair.iteritems():
			print i+1,'. %s:%s' %(value[1:4],value[5:])
			i=i+1
			currpairlist.append(value)
		inp=int(raw_input('Choose pair number:'))
		if inp<=len(currpairlist):
			pair=currpairlist[inp-1]
			break
		currpairlist=[]
		

def callFunction(funName):
	if pripub[funName]=='pri':
		try:
			result=k.query_private(funName)
		except Exception as e:
                        print "An Error occured" + e
			return '0'
	else:
		try:
			result=k.query_public(funName)

		except Exception as e:
			print "An Error occured while calling %s" +  str(e) %funName
			return '0'
	return result

def getOHLC(interval):
	try:
			currtime= int(time.time())
			result=k.query_public('OHLC',{'pair':pair,'interval':interval,'since':currtime-int(interval)*60})
			
			print result['result'][pair][0]
			[timeatserver,openprice,high,low,closeprice,vwap,volume,count]=result['result'][pair][0]
			print low,':',high,':',volume
	except Exception as e:
		print "An Error occured while getting OHLC info", str(e)
		return '0'

#getOHLC('15')
def getAccountBalance():
	result=callFunction('Balance')
	if not result=='0':
		for key,value in result['result'].iteritems():
			print key[1:],':',value
		#get total trade balance: combined balance of all crypto+curr
		result=k.query_private('TradeBalance',{'asset':'ZEUR'})
		if not result=='0':
			print 'Total Balance in EURO:',result['result']['eb']
				
def getAccountBalancebot():
	try:
		result=callFunction('Balance')
		return [result['result']['X%s' %base],result['result']['Z%s' %counter]]
	except Exception as e:
		print e
		return 0,0
def getOpenOrders():
	result=callFunction('OpenOrders')
	openOrders=result['result']['open']
	orderlist=[]
	i=0
	for refid, value in openOrders.iteritems() :
		orderlist.append(refid)
		i+=1
		print i,'. Open:',refid, value['descr']['order'], 'Vol Rem', float(value['vol'])-float(value['vol_exec'])
	if not len(orderlist)>0:
		print "No open orders! Create some"
		return
	while(1==1):
		inp=raw_input('Cancel? Enter number or all to cancel all orders, q quit:')
		if inp=='q':
			break
		elif inp=='all':
			for txid in orderlist:
				ret=cancelOpenOrder(txid)
		elif inp.isdigit():
			ret=cancelOpenOrder(orderlist[int(inp)-1])
		else:
			print "Invalid selection:"
def getOpenPositions():
	try:
		result=k.query_private('OpenPositions')
		volume=0.0000
		cost=0.0000
		for refid, value in result['result'].iteritems() :
			volume+=float(value['vol'])
			cost+=float(value['cost'])
		if not volume==0.00:
			print 'Volume:',volume, '@', cost/volume
		else:
			print "No open position."
	
	except Exception as e:
                print "An Error occured while fetching orders" +  str(e)

def cancelOpenOrder(txid):
	try:
		result=k.query_private('CancelOrder',{'txid':txid})
		return 1
	except Exception as e:
                print "An Error occured while cancelling order" +  str(e)
		return 0
def Ticker(runAlways):
	commadelimitedcurrpair
	while (1==1):
                try:
                        ticker= k.query_public('Ticker',{'pair':commadelimitedcurrpair})
			for pair in currpairlist:
				print ticker['result'][pair]
				print t.getTick(ticker['result'][pair],'ask')
#                        print ticker
                except Exception as e:
                        print "An Error occured while fetching" + pair + str(e)
                        time.sleep(5)
                        continue
#                ask=float(ticker['result'][pair]['a'][0])
#                bid=float(ticker['result'][pair]['b'][0])
#                lastTrade=float(ticker['result'][pair]['c'][0])
#                volumeToday=float(ticker['result'][pair]['v'][0])
#                volumeWeightedAverage=float(ticker['result'][pair]['p'][0])
#                numberOfTrades=float(ticker['result'][pair]['t'][0])
#                lowestToday=float(ticker['result'][pair]['l'][0])
#                HighestToday=float(ticker['result'][pair]['h'][0])
#                openToday=float(ticker['result'][pair]['o'][0])
                if runAlways=='no':
			return
#                        return [ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]
#                print "Ask:%s , Bid:%s , Last Trade:%s , lowest:%s , Highest:%s" %(ask,bid,lastTrade,lowestToday,HighestToday)
#                time.sleep(2)

def getTickerInformation(pair,runAlways):
	
	while (1==1):
		try:
			ticker= k.query_public('Ticker',{'pair':pair})
			#print ticker
		except Exception as e:
			print "An Error occured while fetching" + pair + str(e)
			time.sleep(5)
			continue
		ask=float(ticker['result'][pair]['a'][0])
		bid=float(ticker['result'][pair]['b'][0])
		lastTrade=float(ticker['result'][pair]['c'][0])
                volumeToday=float(ticker['result'][pair]['v'][0])
                volumeWeightedAverage=float(ticker['result'][pair]['p'][0])
                numberOfTrades=float(ticker['result'][pair]['t'][0])
                lowestToday=float(ticker['result'][pair]['l'][0])
                HighestToday=float(ticker['result'][pair]['h'][0])
                openToday=float(ticker['result'][pair]['o'][0])
                if runAlways=='no':
                        return [ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]
		if base=='XDG':
			print "Ask:%s , Bid:%s , Last Trade:%s , lowest:%s , Highest:%s" %('{0:.9f}'.format(ask),'{0:.9f}'.format(bid),'{0:.9f}'.format(lastTrade),'{0:.9f}'.format(lowestToday),'{0:.9f}'.format(HighestToday))
                else:
			print "Ask:%s , Bid:%s , Last Trade:%s , lowest:%s , Highest:%s" %(ask,bid,lastTrade,lowestToday,HighestToday)
                time.sleep(2)



def trade(tradetype,leverage,coins):
	if not leverage=='5m':
		limitPrice=raw_input('Limit price:')
	#	if float(limitPrice)<1000.000 or float(limitPrice)>1300.000:
#			print "Probably wrong selection!"
#			return
		coins=raw_input('%s to %s:' %(base,tradetype))
	ask=0
	bid=0
#	[ask,bid]==getTickerInformation('XXBTZEUR','no')
#	print "Ask:%s || Bid:%s" %(ask,bid)
	print "%sing %s for you:" %(tradetype,base)
	order={'pair': pair,'type': tradetype,'volume': coins,'trading_agreement' : 'agree'}
	if leverage=='5' or leverage=='3' or leverage=='2':
		print "here"
		order.update({'ordertype': 'limit','price': limitPrice,'leverage':leverage})
	elif leverage=='5m':
		leverage=5
		order.update({'ordertype': 'market','leverage':leverage})
	elif leverage=='0':
		order.update({'ordertype': 'limit','price': limitPrice})
	try:
		print "sending order now:%s" %str(datetime.now())
		result=k.query_private('AddOrder', order)
		print "Received result at:%s" %str(datetime.now())
		print result
	except Exception as e:
		print "Error:" + str(e)
def bottrade(pair,tradetype,coins,price):
	order={'pair': pair,'type': tradetype,'volume': coins,'trading_agreement' : 'agree','ordertype': 'limit','price': price,'oflags':'fciq'}
	try:
		result=k.query_private('AddOrder', order)
	except Exception as e:
		print e
		return int(0)
	return result

def botbuy(coins):
		boughtflag=0
		[ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
		spread=ask-bid
		txid=''
		checkflag=0
		if spread>0.14:
			buyat=str(float(bid)+0.00001)
			result= bottrade(pair,'buy',coins,buyat)
#			print "Buying %s@%s" %(coins,buyat)
			if result==0:
				print "result came 0"
				return
			txid =str(result['result']['txid'][0])
			while(1==1):
#				print "C:%s" %checkflag
                                time.sleep(6)
                                [fee,volexec]=QueryOrders(txid)
				if float(volexec)>0.0:
					ret=cancelOpenOrder(txid)
					break
                                if float(volexec)==float(coins):
#					print "Bought: %s@" %volexec,buyat
                                        boughtflag=1
                                        break
				else:
					[asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
					if (float(asknew)-float(buyat)<0.14) or float(bidnew)>float(buyat)+0.00005:
						ret=cancelOpenOrder(txid)
						print 'curr ask:',asknew,' bid:',bidnew,' my bid:',buyat,'diff:',float(asknew)-float(buyat)
#						checkflag=1
						break
#			print "Check flag%s" %checkflag
                        if not boughtflag==1:
#				print "before this"
#                                ret=cancelOpenOrder(txid)
				[basebalance,counterbalance]=getAccountBalancebot()
				if not float(basebalance)==0:
					print "%s:Bought.. %s@" %(str(datetime.now()),float(basebalance)),buyat
				return basebalance,counterbalance
			else:
#				print "before this one"
				[basebalance,counterbalance]=getAccountBalancebot()
				if not float(basebalance)==0:
					print "%s:Bought. %s@" %(str(datetime.now()),float(basebalance)),buyat
				return basebalance,counterbalance
		else:
			return 0,11111.0
def botbetabuy(coins,ask,bid):
        	boughtflag=0
#	        [ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
	        spread=ask-bid
        	txid=''
	        checkflag=0
		volexec=0.0
	        if spread>0.0000002:
                	buyat=str(float(bid)+deci[base])
        	        result= bottrade(pair,'buy',coins,buyat)
	                print "Buying %s@%s" %(coins,buyat)
        	        if result==0:
	                        print "result came 0"
        	       	        return 0,0
                        txid =str(result['result']['txid'][0])
                        while(1==1):
#                               print "C:%s" %checkflag
                                time.sleep(10)
                                [fee,volexec]=QueryOrders(txid)
                                if float(volexec)>0.0:
					if float(volexec)<coins:
						time.sleep(10)
                                        ret=cancelOpenOrder(txid)
					[fee,volexec]=QueryOrders(txid)
                                        break
                                if float(volexec)==float(coins):
                                        boughtflag=1
                                        break
                                else:
                                        [asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
                                        if float(bidnew)>float(buyat)+2*deci[base]:
                                                ret=cancelOpenOrder(txid)
						[fee,volexec]=QueryOrders(txid)
                                                #print 'curr ask:',asknew,' bid:',bidnew,' my bid:',buyat,'diff:',float(asknew)-float(buyat)
#                                               checkflag=1
                                                break
			return [volexec,buyat]
		return 0,0
def botbetasell(coins,sellat):
                txid=''
                soldflag=0
		while(1==1):
	                result=bottrade(pair,'sell',coins,sellat)
                	if result==0:
				time.sleep(2)
                        	continue
                	else:
        	        	print "Selling %s@%s" %(coins,sellat)
                        	txid =str(result['result']['txid'][0])
				break
#               print "Selling %s@" %coins,sellat
                while(1==1):
                        time.sleep(10)
                        [fee,volexec]=QueryOrders(txid)
                        #In case query order caught an exception
			if volexec==coins:
#                               print "Sold %s@" %volexec,sellat
                                soldflag=1
				break
def botsell(coins):
		txid=''
		soldflag=0
		[ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
		sellat=float(ask)-0.00003
		result=bottrade(pair,'sell',coins,sellat)
		print "Selling %s@%s" %(coins,sellat)
		if result==0:
			return
		else:
			txid =str(result['result']['txid'][0])
#		print "Selling %s@" %coins,sellat
		for x in range(1,8):
			time.sleep(6)
			[fee,volexec]=QueryOrders(txid)
			if volexec==coins:
#				print "Sold %s@" %volexec,sellat
				soldflag=1
				break
			else:
                                [asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
                                if (float(sellat)-float(asknew)>0.00010):
                                        ret=cancelOpenOrder(txid)
                                        print 'curr ask:',asknew,' bid:',bidnew,' my bid:',sellat,'diff:',float(sellat)-float(asknew)
#                                       checkflag=1
                                        break

	
		if not soldflag==1:
			ret=cancelOpenOrder(txid)
			[basebalance,counterbalance]=getAccountBalancebot()
			if not coins-float(basebalance)==0.0:
				print "%s:Sold: %s@" %(str(datetime.now()),(coins-float(basebalance))),sellat
			return basebalance,counterbalance
		else:
			[basebalance,counterbalance]=getAccountBalancebot()
			print "%s:Sold. %s@" %(str(datetime.now()),coins),sellat
			return  basebalance,counterbalance
def inputcoins():
	return float(raw_input("How many %s to Trade:" %base))
def buynow(coins,spread):
	[ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
        ask=float(ask)
        bid=float(bid)
        volexec=0.0
        buyat=0.0
	if ask-bid>spread:
		[volexec,buyat]=botbetabuy(coins,ask,bid)
	else:
		return  0.0,0.0
	if float(volexec)>=0.01:
		print "%sBought %s@%s" %(str(datetime.now()),volexec,buyat)
		return float(volexec),float(buyat)
	else:
		 print "Didn't buy"
		 return 0.0,0.0
	return float(volexec),float(buyat)
def sellnow(coins):
	[ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
	result=bottrade(pair,'sell',coins,float(ask)-0.00001)
	txid =str(result['result']['txid'][0])
        print "%s:%s:Order put to sell%s@%s" %(str(datetime.now()),txid,coins,float(ask)-0.00001)
	return txid
def sellnow(coins,sellingprice):
        #[ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
	print coins,'@',sellingprice
        result=bottrade(pair,'sell',coins,sellingprice)
        txid =str(result['result']['txid'][0])
        print "%s:%s:Order put to sell%s@%s" %(str(datetime.now()),txid,coins,sellingprice)
        return txid

def betaalt():
        coins=raw_input("How many %s to Trade:" %base)
	upperlimit=float(raw_input("Never buy Limit:" ))
	profitpercentage=float(raw_input("Profit Percentage? [0.5]:" ) or '0.5')
        while(1==1):

                [ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
                ask=float(ask)
                bid=float(bid)
		volexec=0.0
		buyat=0.0
		if bid>upperlimit or bid>volumeWeightedAverage:
			#print "ask above limit"
			time.sleep(50)
			continue
		else:
	                [volexec,buyat]=botbetabuy(coins,ask,bid)
                if float(volexec)>=0.01:
                        print "%sBought %s@%s" %(str(datetime.now()),volexec,buyat)
			sellingprice=float(buyat)+(profitpercentage*float(buyat)/float(100))
                        result=bottrade(pair,'sell',volexec,sellingprice)
                        txid =str(result['result']['txid'][0])
                        print "%s:%s:Order put to sell%s@%s" %(str(datetime.now()),txid,volexec,sellingprice)
			while(1==1):
				time.sleep(10)
				[feesell,volexecsell]=QueryOrders(txid)
				if float(volexecsell)==float(volexec):
					print "%sSold @%s" %(str(datetime.now()),sellingprice)
					break
			

                time.sleep(20)
def beta():
	coinsinitial=raw_input("How many %s to Trade:" %base)
	
	while(1==1):
		[buyvolumeoutstanding,sellvolumeoutstanding,lowestsellpriceoutstanding]=getOutstandingOrderInfo()
		[ask,bid,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
		increase=((bid-lowestToday)/bid)*100 # increase percentage
		decrease=((HighestToday-ask)/HighestToday)*100 #decrease percentage
		coins=float(decrease)*float(coinsinitial) # if decreased more trade more coins, if increased tradde less coins
		if coins>float(coinsinitial)+2:
			coins=float(coinsinitial)+2
		volumerisk=5*int(coins) # adjust risk according to number of coins in hand
#		print increase,decrease
#		exit()
		ask=float(ask)
		bid=float(bid)
#		if ask-bid<0.08:
#			time.sleep(5)
#			continue
#		print buyvolumeoutstanding,sellvolumeoutstanding,lowestsellpriceoutstanding,decrease
		if (sellvolumeoutstanding<volumerisk and bid<lowestsellpriceoutstanding-0.5 and decrease>0.5):
			print buyvolumeoutstanding,sellvolumeoutstanding,lowestsellpriceoutstanding,decrease
			[volexec,buyat]=botbetabuy(coins)
			if float(volexec)>=0.01:
				print "%sBought %s@%s" %(str(datetime.now()),volexec,buyat)
				result=bottrade(pair,'sell',volexec,float(buyat)+0.3)
				txid =str(result['result']['txid'][0])
				print "%s:%s:Order put to sell%s@%s" %(str(datetime.now()),txid,volexec,float(buyat)+0.3)

		time.sleep(20)

def getOutstandingOrderInfo():
	while(1==1):
		result=callFunction('OpenOrders')
		if result=='0':
			print "Error calling callfunction for openorders"
			time.sleep(10)
			continue
		openOrders=result['result']['open']
		buyvolumeoutstanding=0.0
		sellvolumeoutstanding=0.0
		lowestsellpriceoutstanding=11111.0
		for refid, value in openOrders.iteritems():
			if value['descr']['type']=='sell':
				sellvolumeoutstanding=sellvolumeoutstanding+float(value['vol'])-float(value['vol_exec'])
				if float(value['descr']['price'])<lowestsellpriceoutstanding:
					lowestsellpriceoutstanding=float(value['descr']['price'])
			if value['descr']['type']=='buy':
				buyvolumeoutstanding=buyvolumeoutstanding+float(value['vol'])-float(value['vol_exec'])	
		return float(buyvolumeoutstanding),float(sellvolumeoutstanding),float(lowestsellpriceoutstanding)
def botbeta():
	coins=raw_input("How many %s to Trade:" %base)
	while(1==1):
#		print "trying to buy"
		[volexec,buyat]=botbetabuy(coins)
		if float(volexec)>=0.01:
			print "Bought %s@%s" %(volexec,buyat)
			[asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
			sellat=10000.0
			if float(asknew)>float(buyat)+0.16:
				sellat=float(asknew)-0.00005
			else:
				sellat=float(buyat)+0.16
			botbetasell(volexec,sellat)
			print "Sold %s@%s" %(volexec,sellat)
			print "Just waiting"
			time.sleep(60)
def bot():
	totalfee=0.00
	totalprofit=0.0000
	counterbalance=''
	basebalance=''
	[basebalance,counterbalance]=getAccountBalancebot()
	basebalancenew=basebalance
	counterbalancenew=counterbalance
	startingbalance=counterbalance
	while(1==1):
		coins=5
		if float(basebalancenew)>=0.01:
			[basebalancenew,counterbalancenew]=botsell(float(basebalancenew))
#			[bsebalancenew,counterbalancenew]=getAccountBalancebot()
		else:
			while(1==1):
				[basebalancenew,counterbalancenew]=botbuy(coins)
				if float(basebalancenew)==0.0:
					time.sleep(5)
				else:
					break
#		[bsebalancenew,counterbalancenew]=getAccountBalancebot()
		if not float(counterbalancenew)==11111.0:
			if float(basebalancenew)==0.0:
				profit=(float(counterbalancenew)-float(counterbalance))
				totalprofit=float(counterbalancenew)-float(startingbalance)
				counterbalance=counterbalancenew
				print "%s:Profit last trade:%s , Total:%s" %(str(datetime.now()),profit,totalprofit)
				if float(counterbalance)<10000.0:
					print "Lost, I should not run"
					exit()
				if profit<-0.08:
					print "%s:Not earning" %(str(datetime.now()))
					time.sleep(100)


		else:
			print "I got return from 1111.0"	
def CoinsToTrade(asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday,coins):
	return coins
def tasker():
	while (1==1):
		task=str(raw_input('b=buy,s=sell,bl=buy lev, sl=sell lev, oo=open orders, op=open positions,c=cancel,bal=balance ')).lower()
	#Input:xy1234.000 
	#x=b or s. b for buy. s for sell
	#y=l or m. L for limit , m for market

		if task == 't':
			getTickerInformation(pair,'y')

		if task=='b':
			trade('buy','0','0')
		if task=='bl':
			if base=='ETH':
	                        lev='3'
			elif base=='REP' or base=='ETC':
				lev='2'
        	        else:
                	        lev='5'
			trade('buy',lev,'0')
		if task=='s':
			trade('sell','0','0')
		if task=='sl':
			if base=='ETH':
				lev='3'
			elif base=='REP' or base=='ETC':
                                lev='2'
			else:
				lev='5'
			trade('sell',lev,'0')

		if task=='oo': #query open orders
			getOpenOrders()
		if task=='op': #query open positions
			getOpenPositions()
		if task=='c': #to cancel open orders
			ret=cancelOpenOrder()
		if task=='bal': #get asset info
			getAccountBalance()
		if task=='q':
			break
		if task=='bot':
			print "dangerous business"
			#bot(
	#tries to buy when spread>fees+ and sells@ask minus bit #Problem: stuck on one high price sell order. price goes down, bot waits
		if task=='botbeta':
			botbeta()
	#try to sell @bought+0.5, don't buy over high price if there is any outstanding order with bit high price. Buys when price is again lower than outstanding sell order minus 0.5 
		if task=='beta':
			beta()
		if task=='betaalt':
			betaalt()
		if task=='ticker':
			t.getTicker(k)
		if task=='runticker':
			t.runTicker(k)
		if task=='buysell':
#			minsellpercentage=0.6
			minsellpercentage=float(str(raw_input("Minimum profit percentage?[0.4]:" ))) or float('0.4')
			spread=float(str(raw_input("Spread?[0.1]:" ))) or float('0.1')
			coins=inputcoins()
			while(1==0):
				[asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
				if asknew>0.0455:
					break
				else:
					time.sleep(50)
			while(1==1):
				[volexec,buyat]=buynow(coins,spread)
				if volexec>0.01:
	     				[asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
					if asknew>float(buyat)+((minsellpercentage*float(buyat))/100):
						sellingprice=asknew-2*deci[base]
					else:
						sellingprice=float(buyat)+(minsellpercentage*float(buyat)/100)
					txid=sellnow(volexec,sellingprice)
					i=0
					while(1==1):
						time.sleep(15)
						[feesell,volexecsell]=QueryOrders(txid)
						i=i+1
						if i>400:
							print "Couldn't sell last one due to price fall. timeout. moving to open new buy session"
							break
						if i%20==0:
							[asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
							if asknew<sellingprice-percent.percent(3,sellingprice):
								print "Couldn't sell last one. went low by 12 percent, I'll skip and create new trades"
								break
#						if i%5==0:
#                                                    [asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
#						    if asknew+5*deci[base]<sellingprice:
#							ret=cancelOpenOrder(txid)
#							time.sleep(5)
#							[feesell,volexecsell]=QueryOrders(txid)
#							if ret==1:
#								[asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
#								if asknew>float(buyat)+((minsellpercentage*float(buyat))/100):
#			                                                sellingpricenew=asknew-2*deci[base]
#                        			                else:
#                                                			sellingpricenew=float(buyat)+(minsellpercentage*float(buyat)/100)
#								if not float(volexecsell)==float(volexec):
#				                                        txid=sellnow(float(volexec)-float(volexecsell),sellingpricenew)
#								continue
				
						soldpercentage=(float(volexecsell)/float(volexec))*100
						#if 80% is sold then we consider it all sold and move on.
		                                if soldpercentage>80:
        		                                print "%s Sold %s percent @%s" %(str(datetime.now()),soldpercentage,sellingprice)
						        time.sleep(10)	
							break
				else:
					time.sleep(5)
		if task=='buynow':
		    while(1==1):
			[volexec,buyat]=buynow(inputcoins(),deci[base])
			if not volexec==0.0:
				for i in range(3,8,1):
					print 'Profit ',float(i)/10.0,'% Sell@:',buyat+((float(i)/10.0)*buyat/float(100))
				sellornot=raw_input("sell? y/n [y] :" ) or 'y'
				if sellornot=='y':
					txid=sellnow(volexec)		
			else:
				buyagain=raw_input("Buy again y/n [y] or open orders :" ) or 'y'
				if buyagain=='y':
					continue
				if buyagain=='n':
					break
				if buyagain=='oo':
					getOpenOrders()
		if task=='sellnow':
			[asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
			txid=sellnow(inputcoins(),float(asknew)-deci[base])
	#Buysell using volume weighted average
		if task=='vwa':
		    coins=inputcoins()
		    spread=float(str(raw_input("Spread?[0.1]:" ))) or float('0.1')
		    while(1==1):
			signal=d.shouldIBuy(pair)
			print signal
			if  signal=='Buy Signal':
				print "its buy time"
	                        while(1==1):
        	                        [volexec,buyat]=buynow(coins,spread)
                	                if volexec>0.01:
                        	                [asknew,bidnew,lastTrade,volumeWeightedAverage,lowestToday,HighestToday]=getTickerInformation(pair,'no')
						percentage=float(buyat)+((0.5*float(buyat))/100)
                                	        if asknew>percentage:
                                        	        sellingprice=asknew-0.00002
	                                        else:
        	                                        sellingprice=percentage
                	                        txid=sellnow(volexec,sellingprice)
                        	                while(1==1):
                                	                [feesell,volexecsell]=QueryOrders(txid)
                                        	        if float(volexecsell)==float(volexec):
                                                	        print "%sSold @%s" %(str(datetime.now()),sellingprice)
                                                        	time.sleep(10)
	                                                        break
        	                                        else:
                	                                        time.sleep(10)
						break
                        	        else:
                                	        time.sleep(5)

			time.sleep(600)

while(1==1):
        chooseCurrPair()
        base=pair[1:4]
        counter=pair[5:]
        print pair,base,counter
        tasker()

