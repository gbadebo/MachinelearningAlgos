
import os
import string
from sets import Set
import math

import sys

#Get all unique words in all doc
punc = string.punctuation
ham_list = []
countofAllDocHam = 0;
for (path, dirs, files) in os.walk('./train/ham'):
	for myfile in files:
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		s = list(content)
		tokens = ''.join([o for o in s if not o in punc]).split()
		ham_list.extend(tokens)
		countofAllDocHam = countofAllDocHam + 1
		fs.close()

countofAllDocSpam = 0;

spam_list = []
for (path, dirs, files) in os.walk('./train/spam'):
	for myfile in files:
		
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		s = list(content)
		tokens = ''.join([o for o in s if not o in punc]).split()
		spam_list.extend(tokens)
		countofAllDocSpam = countofAllDocSpam + 1
		fs.close()

countofAllDoc = countofAllDocHam + countofAllDocSpam
full_list = []
full_list.extend(ham_list)
full_list.extend(spam_list)

AllUniqWords  = Set(full_list)

#===========================================================
# to remove stop words
removestop = sys.argv[1]

if removestop == 'yes':
	so=open( "stopwords")
	stopwords = []		
	for line in so:
		stopwords.append(line.replace('\n', '').replace('\r', ''))

	so.close()	
	uniqstop = Set(stopwords)



	AllUniqWords -= uniqstop

#=========================================================================

countDoc = [countofAllDocSpam, countofAllDocHam]

ListOfDoc = [spam_list,ham_list]
classlabel = [0,1]

prior = {}
condProb = {}
for c in classlabel:
	prior[c] = float(countDoc[c] / countofAllDoc)
	
	for t in AllUniqWords:
		#count occurence of t in files in class c
		countofT = 1.0
		for word in ListOfDoc[c]:
			if word == t:
				countofT = countofT + 1

		condProb[t + "_" + str(c)] = float(countofT/(len(ListOfDoc[c]) + len(AllUniqWords)))




#testing

def test(filename,knownclass):
	allcount = 0.0
	predclassCount = 0.0
	for (path, dirs, files) in os.walk(filename):
		for myfile in files:
			allcount = allcount + 1.0
			score = {}
			fs=open( os.path.join(path, myfile))
			content = fs.read()
			s = list(content)
			tokens = ''.join([o for o in s if not o in punc]).split()
			fs.close()
		
			for c in classlabel:
				score[c] = prior[c]
				for word in tokens:
					key =  word + "_" + str(c)
					if key in condProb:
						
						score[c] = score[c] + math.log(condProb[key])

			
			maxclass = 0
			if(score[0] > score[1]) : 
				maxclass = 0
			else:
				maxclass = 1
			
			if maxclass == knownclass:
				predclassCount = predclassCount + 1.0

	print predclassCount
	print allcount
	print "accuracy = " + filename + " " + str(float(predclassCount/allcount) )
	

test('./test/ham',1)

test('./test/spam',0)
