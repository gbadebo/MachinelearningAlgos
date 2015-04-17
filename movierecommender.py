import math
from string import split
from sets import Set
import time
from operator import itemgetter
import random
import sys

def timer():
   now = time.localtime(time.time())
   return now[5]
#1,501,1001
myrange = int(sys.argv[1])


fs=open( "TrainingRatings.txt")
dataList={}
Uniqueuserids = Set()
UniquemovieIds = Set()
#Read training data
for line in fs:
	line = line.replace('\n', '').replace('\r', '')
	lineSplit=split(line,",")
	movieid = lineSplit[0]
	userid = lineSplit[1]
	
	Uniqueuserids.add(userid)
	UniquemovieIds.add(movieid)
	recordTuple = (userid,movieid)	
	dataList[recordTuple] = lineSplit[2]

fs.close()
	
print len(Uniqueuserids)
print len(UniquemovieIds)
print len(dataList)



#compute vbar_i average rating given by each user to all items the user rated
averageUserRateAllItems = {}
for user in Uniqueuserids:
	sum=0.0
	count = 0.0
	for item in UniquemovieIds:
		if (user,item) in dataList:
			count = count +1.0
			sum = sum + float(dataList[(user,item)])
	
	averageUserRateAllItems[user] = sum/count

	
			
#print averageUserRateAllItems
cacheWeightCorr = {} # to reduce duplicate calculations
#calculate correlation between the input user and all other users
def calcWeightCorr(user1):
	current_sec = timer()
	weightCorrelations = {}
	for user2 in Uniqueuserids:
		if user1 != user2:
			#shift if correlation already calculated then just copy data
			if (user1,user2) in cacheWeightCorr:
				weightCorrelations[(user1,user2)] = cacheWeightCorr[(user1,user2)]
			elif (user2,user1) in cacheWeightCorr:
				weightCorrelations[(user1,user2)] = cacheWeightCorr[(user2,user1)]
			else:
				uppersum = 0.0
				lowersumpart1 = 0.0
				lowersumpart2 = 0.0
				#loop over items
				for movie in UniquemovieIds:
					if (user1,movie) in dataList:
						if (user2,movie) in dataList:
							part1 = float(dataList[(user1,movie)])-averageUserRateAllItems[user1]
							part2 = float(dataList[(user2,movie)])-averageUserRateAllItems[user2] 

							uppersum = uppersum + part1*part2
							lowersumpart1 = lowersumpart1 +  part1* part1
							lowersumpart2 = lowersumpart2 + part2*part2
			

				#compute w(user1,user2)
				if lowersumpart1 == 0 or lowersumpart2 == 0:
					weightCorrelations[(user1,user2)] = 0.0
				else:

					weightCorrelations[(user1,user2)] = 	uppersum/math.sqrt(lowersumpart1 * lowersumpart2)	
	#print str(timer() - current_sec )			
	return weightCorrelations		





#myweightCorrelations = calcWeightCorr('1942739')
#print myweightCorrelations


#sumofWeightCorr = 0.0
#for key in myweightCorrelations:
#	sumofWeightCorr = sumofWeightCorr + myweightCorrelations[key]

#print sumofWeightCorr



#prediction eqaution

fs=open( "TestingRatings.txt")
testList = []
for line in fs:
	line = line.replace('\n', '').replace('\r', '')
	lineSplit=split(line,",")
	movieid = lineSplit[0]
	userid = lineSplit[1]
	rating = lineSplit[2]
	recordTuple = (userid,movieid,rating)	
	testList.append(recordTuple)

fs.close()
testList = sorted(testList,key=itemgetter(0))  #to increase locality of cache access 
sumofError = 0.0
sumofSqError = 0.0
print "userid movieid pred_rating orig_rating error "

totalsumlen = 0


#for start in range(1,len(testList), 1000):
for start in range(myrange,myrange+500, 100):
	testDict = {}
	errorDict = {}
	readDict={}
	

	#start = random.randint(1, 50000)
	for myRecord in testList[start:start+100]:
		userid = myRecord[0]
		movieid = myRecord[1]
		myweightCorrelations = calcWeightCorr(userid)
		#print userid
		cacheWeightCorr.update(myweightCorrelations)   # to reduce recalculation of weight
		#print "cache len " + str(len(cacheWeightCorr))
		sumofWeightCorr = 0.0
		for key in myweightCorrelations:
			#note all key is a tuple of two users a,i where key(0) is constant and key(1) is varying
			#all records not present in this dictionary is counted as have correlation of  0
			#it possible that i never rated movie with movieid so skip
			recordTuple = (key[1],movieid)	
			if recordTuple in dataList:
				sumofWeightCorr = sumofWeightCorr + myweightCorrelations[key]* (float(dataList[recordTuple]) -averageUserRateAllItems[key[1]] )
	
		sumofDenWeightCorr =0.0
		for key in myweightCorrelations:
			sumofDenWeightCorr = sumofDenWeightCorr + abs(myweightCorrelations[key])

		if sumofDenWeightCorr== 0.0:
			sumofDenWeightCorr = 1.0
		testDict[(userid,movieid)] = averageUserRateAllItems[userid] + sumofWeightCorr/sumofDenWeightCorr #predicted rating
		errorDict[(userid,movieid)] = testDict[(userid,movieid)] -  float(myRecord[2])
		readDict[(userid,movieid)] = float(myRecord[2])


	#print testDict
	#print errorDict
	
	#for key in testDict:
	#	print "" + str(key[0]) + " " + str(key[1]) + " "+ str(testDict[key]) + " " + str(readDict[key]) + " "+ str(errorDict[key])
	
	for key in errorDict:
		sumofError = sumofError + abs(errorDict[key])

	#print "PARTIAL SUM ERROR: " + str(sumofError)
	totalsumlen = totalsumlen + len(errorDict)
	#print "len: " + str(totalsumlen)
	for key in errorDict:
		sumofSqError = sumofSqError + errorDict[key] * errorDict[key]


	#print "PARTIAL SUM SQ ERROR: " + str(sumofSqError)

print "Starting at " + str(myrange) + "To " + str(myrange+500)
print "SumAE " + str(sumofError)
print "Len "	+str(totalsumlen)
print "MAE " + str(sumofError/totalsumlen)


print "RMSE " + str(math.sqrt(sumofSqError/totalsumlen))

print "SUMSE " + str(sumofSqError)
print "Len "   +str(totalsumlen)


print "========================================================================="
print "========================================================================="
print "========================================================================="
print "" 
print ""
