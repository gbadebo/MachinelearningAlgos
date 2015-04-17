import math
from string import split

class Instance:
	def __init__(self,mylabel,myinstance):
		self.label = mylabel
		self.instancevar = myinstance
		self.datalen=0

class LogRegres:
	def __init__(self):
       		self.rate = 0.01
		self.weight = []
		self.TrainInstances = [] # list that contains list of instance object
      


	def loadData(self , filename):
		fs=open( filename)
		lenght = 0
		for line in fs:
			lineSplit=split(line," ")
			numOfCol = len(lineSplit)
			label = lineSplit[numOfCol-1]
			instance = lineSplit[0:numOfCol-1] # note hear to load instances as nothing is hardcoded
			lenght = len(instance)
			MyInstance =  Instance(label,instance)
			self.TrainInstances.append(MyInstance)						
		fs.close()
		self.datalen = lenght
		
		

	def sigmoid(self, z):
		return 1 / (1 + math.exp(-z));

	
	def train(self,iterations,bias):
		self.weight = [0.0] * self.datalen
		for i in range(iterations):
			lik = 0.0
			for myinstance in self.TrainInstances:
				predicted = self.classify(myinstance.instancevar)
				label =float( int(myinstance.label))
				for j in range(len(self.weight)-1):
					self.weight[j] = self.weight[j] + self.rate * (label - predicted) * float(myinstance.instancevar[j]) - (self.rate * bias * self.weight[j] ) ;
				lik += label * math.log(self.classify(myinstance.instancevar)) + (1-label) * math.log(1- self.classify(myinstance.instancevar));
			#print str(i)+ " likelihood =" +str(lik)
	

	def classify(self,instance):
		logit = 0.0
		for i in range(len(self.weight)-1): 
			logit += self.weight[i] * float(instance[i]);
		return self.sigmoid(logit);
	


	


myWork =  LogRegres()

myWork.loadData('data.txt')
#regL2 = [ 0.0,.01,.02,.05,.1,.5,1.0,2.0,3.0,4.0,5.0,6.0,7.0,10.0]
regL2 = [ 0.0,.01,10.0]

for val in regL2:
	

	myWork.train(20,val)  #best for now at 10,0.01


	print "RegL2 = "+str(val)
	fs=open( "test.txt")
	count=0
	countright=0		
	for line in fs:
		lineSplit=split(line," ")
		testdata = lineSplit[0:-1]
		count = count + 1
		#print testdata
		#print lineSplit[-1]
		prob = myWork.classify(testdata)
		#print "prob(1|x) = " + str(prob)
		if prob > 0.15 and count < 348:
			countright= countright + 1
		if prob < 0.15 and count > 348:
			countright= countright + 1


	print "With accuracy = " + str(float(float(countright)/float(count)))
	print "---------------------------------------------"
	print "---------------------------------------------\n"

	



