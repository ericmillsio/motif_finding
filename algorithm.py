import sys
import numpy


mapper = { 'A': 0, 'C': 1, 'T': 3, 'G': 2}
revMapper = {  0:'A',  1:'C',  3:'T' ,  2:'G'}
sites = {}

def hammingDistance(str1,i, str2, j, length):
	dist = 0
	for x in range(0, length):
		if str1[i+x] is not str2[x+j]:
			 dist+=1
	return dist  


def getBestSubstringPair(str1, str2, length):
	index1 = 0;
	index2 = 0;
	bestScore = length;
	for i in range(0, len(str1)-length):
		for j in range(0, len(str2)-length):
			newScore = hammingDistance(str1,i, str2, j, length)
			if newScore < bestScore:
				index1 = i
				index2 = j
				bestScore = newScore	
	return str1[index1:index1+length], str2[index2:index2+length], bestScore

def getSequencesFromFile(fileName):
	lines = open(fileName).read().splitlines()
	return lines[1::2]  



def getScoreMatrix(str1, str2, length):
	
	mat = numpy.zeros([length, 4])
	for i, c in enumerate(str1):
		mat[i][mapper[c]] += 1
	for i, c in enumerate(str2):
		mat[i][mapper[c]] += 1
	return mat


def getMotifInstance(str1, mat, length):
	bestScore = 0;
	bestIndex = 0;
	newScore = 0;
	for i in range(0, len(str1)):
		newScore = getScore(str1[i:i+length], mat)
		if newScore > bestScore:
			bestScore = newScore
			bestIndex = i
	return str1[bestIndex:bestIndex+length], bestIndex

def getScore(str1, mat):
	score = 0
	for i, c in enumerate(str1):
		score += mat[i][mapper[c]]
	return score

def adjustMatrix(str1, mat):
	for i, c in enumerate(str1):
		mat[i][mapper[c]] += 1	

def getMotifMatrix(sequences, length):
	motif1, motif2 = "",""
 	score = length 
	x = -1
	y = -1
	for i in range(0,len(sequences)):
		for j in range(i+1, len(sequences)):
			new_motif1, new_motif2, new_score = getBestSubstringPair(sequences[i], sequences[j], length)
			if(new_score < score):
				score = new_score
				motif1 = new_motif1
				motif2 = new_motif2
				x = i
				y = j
	
	sites[x] = sequences[x].index(motif1)
	sites[y] = sequences[y].index(motif2)

	matr = getScoreMatrix(motif1, motif2, length)
	for i in range(0, len(sequences)):
		if i is x or i is y:
			continue
		motifN , index = getMotifInstance(sequences[i], matr, length)
		
		sites[i] = index
		adjustMatrix(motifN, matr)
		
	return matr
	
def main(argv):
	globalLength = int(open(argv[1]).read())
	sequences = getSequencesFromFile(argv[0])
	matter =  getMotifMatrix(sequences, globalLength)
	# print " ",["A","C","G","T"]
	
	#FOR PRINTING OUTPUT IF RUNNING JUST THIS
	#print matter
	#for i in matter.argmax(1):
	#	print revMapper[i]


	with open("predictedmotif.txt","w") as out_motif:
		out_motif.write(">PREDICTED_MOTIF\n")
		for i in matter.tolist():
			for j in i:
				out_motif.write(str(j)+"\t")
			out_motif.write("\n")
		out_motif.write("<")

	with open("predictedsites.txt","w") as out_sites:
		for k,v in sites.iteritems():
			out_sites.write("seq"+str(k)+"\t"+str(v))
			out_sites.write("\n")
	

if __name__ == "__main__":
	main(sys.argv[1:])	
	

