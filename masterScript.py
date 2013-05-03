import os 
import timing
import math

results = {}
root = os.getcwd()

def fi(fl):
	return int(float(fl))

def addResults(folder):
	os.chdir(root+"/"+folder+"/")
	for k in range(0, 30):
		os.chdir(root+"/"+folder+"/"+str(k))

		result = {}

		result["time"] = timing.run()
		fileActual = open("sites.txt")
		filePredict = open("predictedsites.txt")

		linesActual = fileActual.read().splitlines()	
		linesPredict = filePredict.read().splitlines()	

		count = 0
		
		for i in range(0, len(linesActual)):
			if linesActual[i] == linesPredict[i]:
				count += 1

		result["hits"] = count

		fileActual.close()
		filePredict.close()

		fileNorm = open("norm.txt")
		fileMotifPredicted = open("predictedmotif.txt")

		linesActual = fileNorm.read().splitlines()
		linesPredict = fileMotifPredicted.read().splitlines()
	
		divisor = sum(map(fi,linesPredict[1].split()))
	
		runningSum = 0.0
	
		for i in range(1, len(linesActual)-1):
			numsActual = map(float, linesActual[i].split())
			numsPredict = map(fi, linesPredict[i].split())
			for j in range(0, 4):
				runningSum += numsActual[j] * math.log((numsActual[j]*divisor+0.00001)/(numsPredict[j]+0.00001))

		result["re"] = runningSum

		results[folder+str(k)] = result
		os.chdir(root+"/"+folder+"/")
		print folder, k
	
	os.chdir(root)


addResults("ml")
addResults("icpc")
addResults("sc")

os.chdir(root)

with open("all_results.txt", "w") as f:
	f.write("type,val,re,hits,time\n")
	for i in range(0,30):
		res = results["ml"+str(i)]

		ml = 8
		if i < 10:
			ml = 6
		elif i < 20:
			ml = 7
		f.write("ml," + str(ml) + ",")

		for k, v in res.iteritems():
			f.write(str(v) + ",")
		f.write("\n")

		icpc = 2
		if i < 10:
			icpc = 1
		elif i < 20:
			icpc = 1.5
		f.write("icpc," + str(icpc) + ",")

		res = results["icpc"+str(i)]
		for k, v in res.iteritems():
			f.write(str(v) + ",")
		f.write("\n")

		sc = 20
		if i < 10:
			sc = 5
		elif i < 20:
			sc = 10
		f.write("sc," + str(sc) + ",")

		res = results["sc"+str(i)]
		for k, v in res.iteritems():
			f.write(str(v) + ",")
		f.write("\n")



