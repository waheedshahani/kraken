import time
from datetime import datetime
import krakenex
k=krakenex.API()
k.load_key('/home/ubuntu/kraken/krakenkey.key')

def getTradeHistory():
        try:
                result=k.query_private('TradesHistory',{'type':'all','start':1494876099.7805,'ofss':5})
		print result
        except Exception as e:
                print e
                return [0,0]
#       print result



getTradeHistory()


