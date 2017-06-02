d = {}
currencytocheck=['XXLMZEUR']
buy=['buy']
sell=['sell']
volbought=0.0
volsold=0.0
costbought=0.0
costsold=0.0
feebought=0.0
feesold=0.0
price=0.0
with open("exportedsheet.txt") as f:
	for x in f:
		rows = [[y for y in x.split("\t")[:-1]]]
		cols = [list(col) for col in zip(*rows)]
		d.update({x.split("\t")[0]:cols})
	i=0
	for x,y in d.iteritems():
		vol=float(y[9][0])
		cost=float(y[7][0])
		fee=float(y[8][0])
		if y[2]==currencytocheck:
			if y[4]==buy:
				volbought=volbought+vol
				costbought=costbought+cost
				feebought=feebought+fee
			if y[4]==sell:
				volsold=volsold+vol
				costsold=costsold+cost
				feesold=feesold+fee
	price=float(raw_input('current price?:'))
	print type(price)
	print 'Bought ', volbought , 'Price=',costbought, 'Fee=', feebought
	print 'Sold ', volsold, 'Price=', costsold, 'Fee=', feesold
	print 'Profit=',costsold-costbought-feebought-feesold 
	print 'Extra coins in hand=', volbought-volsold
	volinhand=volbought-volsold
	print 'Total profit=', volinhand*float(price)

