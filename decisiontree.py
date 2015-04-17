from string import split
import math
import operator
from pprint import pprint
import sys


class DecisionTree:

	
	def splitDataset(self,dataset,nclom,value):
		retDataSet=[]
		for record in dataset:
			if record[nclom] == value:
				reducedRecord=record[:nclom]
				reducedRecord.extend(record[nclom+1:])
				retDataSet.append(reducedRecord)
		return retDataSet
	
	
	def buildDecisionTree(self,dataset,labels):
		classlist=[ x[-1] for x in dataset]
		if classlist.count(classlist[0]) == len(classlist):
			return classlist[0]
		if len(classlist)==1:
			return doCountMajority(classlist)
		bestFeature=self.getSplitBestFeature(dataset)
		bestFeatureLabel=labels[bestFeature]
		tree={bestFeatureLabel:{}}
		del(labels[bestFeature])
		featValues = [x[bestFeature] for x in dataset]
		uniqueVals = set(featValues)
		for value in uniqueVals:
			subLabels = labels[:]
			tree[bestFeatureLabel][value] = self.buildDecisionTree(self.splitDataset(dataset, bestFeature, value),subLabels)
		return tree

	def doClassification(self,tree,labels,testvec):
		childKey = tree.keys()[0]
		childTree = tree[childKey]
		featIndex = labels.index(childKey)
		for key in childTree.keys():
			if testvec[featIndex] == key:
				if type(childTree[key]).__name__ == 'dict':
					classLabel = self.doClassification(childTree[key],labels,testvec)
				else: classLabel = childTree[key]
		try:
			return classLabel
		except:
			return 1

	def PrintTree(self,tree,count):
		for key, value in tree.items() :
    			if type(tree[key]).__name__ == 'dict':
				print (str(key)+  "=" + str(value.keys()[0]))
				space = ""
				for i in range(0,count):
					space = space + " "
				print space
				count = count+1
				self.PrintTree(value,count)
			else: print (str(key) + " = " + str(value))

	def doCountMajority(self,classlist):
		classcount={}
		for vote in classlist:
			if vote not in classcount.keys():
				classcount[vote]=0
			classcount[vote] += 1
		sortedClassCount=sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
		return sortedClassCount[0][0]
	
	def entropy(self,dataset):
		n=len(dataset)
		labels={}
		for record in dataset:
			label=record[-1]
			if label not in labels.keys():
				labels[label]=0
			labels[label]+=1
		ent=0.0
	# using k0*k1/k*k
		for key in labels.keys():
			prob1=float(labels[key])/n
			prob2 = (n-float(labels[key]))/n
			ent= prob1*prob2
		return ent

	def getSplitBestFeature(self,dataset):
		numberFeature=len(dataset[0])-1
		baseEntropy=self.entropy(dataset)
		maxInfoGain=0.0
		bestFeature=-1
		for i in range(numberFeature):
			featureList=[x[i] for x in dataset]
			uniqueValues=set(featureList)
			newEntropy=0.0
			for value in uniqueValues:
				subDataset=self.splitDataset(dataset, i, value)
				prob=len(subDataset)/float(len(dataset))
				newEntropy = newEntropy + prob*self.entropy(subDataset)
			infoGain=baseEntropy-newEntropy
			if maxInfoGain < infoGain:
				maxInfoGain=infoGain
				bestFeature=i
		return bestFeature

 
	def train(self):
		fs=open(self.nameofTrainFile)
		dataset=[]
		labels=[]
		count = 0
		for line in fs:
			if count == 0:
				lineSplit=split(line[:-1],",")
				for value in lineSplit:
					labels.append(value)
				print labels
				labelen = len(labels)
				labels = labels[:labelen-1]
				print labels
				count = count+1
			else:	
				lineSplit=split(line[:-1],",")
				dataset.append([float(value) for value in lineSplit])
		fs.close()
		nfeature=len(dataset[0])
		self.labels2=[x for x in labels]
		self.tree= self.buildDecisionTree(dataset, labels)
		


	def __init__(self, trainfile,validationfile,testfile,toprint):
		self.nameofTrainFile = trainfile
		self.nameofValidationFile = validationfile
		self.nameofTestFile = testfile
		self.printdectree = toprint

	def PrintDecisionTree(self):
		if self.printdectree == "yes":
			pprint(self.tree)
	
	def testTree(self):
		fs=open(self.nameofTestFile)
		datasetTest=[]
		countTest = 0
		for line in fs:
			if countTest == 0:
				lineSplit=split(line[:-1],",")
				countTest = countTest+1
			else:	
				lineSplit=split(line[:-1],",")
		
				datasetTest.append([float(value) for value in lineSplit])
		fs.close()
		nPos=0
		for r in datasetTest:
			ret= self.doClassification(self.tree, self.labels2, r)
			if ret==r[-1]:
				nPos +=1
		ntest=len(datasetTest)
		print "Accuracy is " + str(nPos/float(ntest))


#python decision.py 2 3 data_sets1/training_set.csv data_sets1/validation_set.csv data_sets1/test_set.csv no

print "<L> <K> <training-set> <validation-set> <test-set> <to-print>"
print "L: integer (used in the post-pruning algorithm)"
print "K: integer (used in the post-pruning algorithm)"
print "to-print:{yes,no}"



L = sys.argv[1]

K = sys.argv[2]

trainingdatafile = sys.argv[3]

validationdatafile = sys.argv[4]

testdatafile = sys.argv[5]

toprint = sys.argv[6]


dec = DecisionTree(trainingdatafile,validationdatafile,testdatafile,toprint)
dec.train()
dec.testTree()
dec.PrintDecisionTree()



	
