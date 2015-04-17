import os


numcentroid = [2,5,10,15,20]

originalSize = os.path.getsize("Koala.jpg")
print "Koala.jpg"
for  k in numcentroid:
	print "K: " +str(k)
	cRatioSum = 0.0;
	for i in range(1,10):
		filename =  "cKoala"+str(k)+ str(i) + ".jpg"		
		filesize = os.path.getsize(filename)		
		cRatioSum = cRatioSum + float(originalSize)/float(filesize)
	cRatioMean = cRatioSum/9.0
	print "Mean Compression Ratio: " + str(cRatioMean)
	
	varSum = 0;
	for i in range(1,10):
		filesize = os.path.getsize(filename)
		compRatio = float(originalSize)/float(filesize)
		varSum = varSum + (compRatio - cRatioMean) * (compRatio - cRatioMean);
	variance = varSum/9.0
	print "Variance Compression Ratio: " + str(variance)
	print "==================================================="
		


originalSize = os.path.getsize("Penguins.jpg")
print "Penguins.jpg"
for  k in numcentroid:
	print "K: " +str(k)
	cRatioSum = 0.0;
	for i in range(1,10):
		filename =  "cPenguins"+str(k)+ str(i) + ".jpg"		
		filesize = os.path.getsize(filename)		
		cRatioSum = cRatioSum + float(originalSize)/float(filesize)
	cRatioMean = cRatioSum/9.0
	print "Mean Compression Ratio: " + str(cRatioMean)
	
	varSum = 0;
	for i in range(1,10):
		filesize = os.path.getsize(filename)
		compRatio = float(originalSize)/float(filesize)
		varSum = varSum + (compRatio - cRatioMean) * (compRatio - cRatioMean);
	variance = varSum/9.0
	print "Variance Compression Ratio: " + str(variance)
	print "==================================================="
	
		



