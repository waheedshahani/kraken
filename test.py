import subprocess
import requests
import time
from datetime import datetime
import sys
datapoints=0
total=0.00
lists=[]
emailThresholdgoingDown=1160.000
emailThresholdgoingUp=1230.000
def mailToWaheed(xbteur):
	cmd="""echo "test" | mailx -s 'test!' waheed.shahani@gmail.com"""
	p=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	output, errors = p.communicate()
	print errors,output
def min(list):
	min = list[0]
	for elm in list[1:]:
		if elm < min:
  			min = elm
	return min
 	print "The minimum value in the list is: " + str(min) 	 
def max(list): 	
	max = list[0] 	 	
	for elm in list[1:]:
 		if elm > max:
			max = elm
	return max	
#print "The maximum value in the list is: " + str(max)
#averaging per number of seconds
averagingFactor=1.00
frequency=1.00 #one request per frequency seconds
#f = open('file.txt', 'w')
while (1==1):
	f = open('file.txt', 'a')
	try:
		a=requests.get('https://blockchain.info/tobtc?currency=EUR&value=1')
	except requests.exceptions.Timeout:
		print "Timedout: Probably network error:"
		time.sleep(5)
		continue
	try:
		a=a.json()
	except ValueError, e:
		print e
		time.sleep(5)
		continue
	a=1.000/a
	if (a<emailThresholdgoingDown) or (a>emailThresholdgoingUp):
		mailToWaheed(a)
		time.sleep(3)
		mailToWaheed(a)
		time.sleep(5)
                mailToWaheed(a)
		time.sleep(5)
                mailToWaheed(a)
		time.sleep(5)
                mailToWaheed(a)
		time.sleep(5)
                mailToWaheed(a)

		exit()
	lists.append(a)
	if len(lists)==int(averagingFactor):
		maxi=min(lists)
		mini=max(lists)
		for p in lists:
			total=total+p
		for p in lists:
			lists.remove(p)
		aver=total/averagingFactor
		f.write("\n%s	AVER	%.3f	MIN	%.3f MAX	%.3f" %(str(datetime.now()),aver,maxi,mini))
#		f.close()
		print ("%s:AVER:%.3f MIN: %.3f MAX: %.3f" %(str(datetime.now()),aver,maxi,mini))
		total=0.00

#	total=total+(1.000/a))
#	print ("%.3f" % a)
#	total=total+a
	time.sleep (1.00)
	time.sleep(1)
#	datapoints=datapoints+1
#	if datapoints==5: 
#		aver=total/60.00
#		print ("%s:%.3f" %(str(datetime.now()),aver))
#		total=0.00
#		datapoints=0

