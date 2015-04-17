
import os
import string
from sets import Set
import sys


punc = string.punctuation
full_list = []
for (path, dirs, files) in os.walk('./train/ham'):
	for myfile in files:
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		s = list(content)
		tokens = ''.join([o for o in s if not o in punc]).split()
		full_list.extend(tokens)
		
		fs.close()



for (path, dirs, files) in os.walk('./train/spam'):
	for myfile in files:
		
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		s = list(content)
		tokens = ''.join([o for o in s if not o in punc]).split()
		full_list.extend(tokens)
		fs.close()
	

print len(full_list)

so=open( "stopwords")
stopwords = []		
for line in so:
	stopwords.append(line.replace('\n', '').replace('\r', ''))

so.close()	
uniqstop = Set(stopwords)

uniqueWords = Set(full_list)

removestop = sys.argv[1]

if removestop == 'yes':

	uniqueWords -= uniqstop



print len(uniqueWords)


fo = open("data.txt", "wb")


for (path, dirs, files) in os.walk('./train/ham'):
	
	for myfile in files:
		#print(len(files))
		line=""
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		for word in uniqueWords:				
			if ( word in content):
				line = line + "1 "
			else:	
				line = line + "0 "
		fs.close()
		line = line + "1\n"
		fo.write( line);
		




for (path, dirs, files) in os.walk('./train/spam'):
	
	for myfile in files:
		#print(len(files))
		line=""
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		for word in uniqueWords:				
			if ( word in content):
				line = line + "1 " #present in file
			else:	
				line = line + "0 "
		fs.close()
		line = line + "0\n"  #labeled as spam
		fo.write( line);
		





fo.close()










#print uniqueWords



fo = open("test.txt", "wb")


for (path, dirs, files) in os.walk('./test/ham'):
	
	for myfile in files:
		#print(len(files))
		line=""
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		for word in uniqueWords:				
			if ( word in content):
				line = line + "1 "
			else:	
				line = line + "0 "
		fs.close()
		line = line + "1\n"
		fo.write( line);
		




for (path, dirs, files) in os.walk('./test/spam'):
	
	for myfile in files:
		#print(len(files))
		line=""
		fs=open( os.path.join(path, myfile))
		content = fs.read()
		for word in uniqueWords:				
			if ( word in content):
				line = line + "1 " #present in file
			else:	
				line = line + "0 "
		fs.close()
		line = line + "0\n"
		fo.write( line);
		





fo.close()
		



