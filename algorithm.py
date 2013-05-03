import sys
import numpy


mapper = { 'A': 0, 'C': 1, 'T': 2, 'G': 3}

def hammingDistance(str1, str2):
	dist = 0
	for i in range(0, len(str1)):
		if str1[i] is not str2[i]:
			 dist+=1
	return dist  


def getBestSubstringPair(str1, str2, length):
	index1 = 0;
	index2 = 0;
	bestScore = length;
	for i in range(0, len(str1)-length):
		for j in range(0, len(str2)-length):
			newScore = hammingDistance(str1[i:i+length], str2[j: j+length])
			if newScore < bestScore:
				index1 = i
				index2 = j
				bestScore = newScore
	return (str1[index1:index1+length], str2[index2:index2+length])

def getSequencesFromFile(fileName):
	lines = open(fileName).read().splitlines()
	return lines[1::2]

def getSequences():
	return getSequencesFromFile(sys.argv[1])

def getScoreMatrix(str1, str2, length):
	
	mat = numpy.zeros([length, 4])
	for i, c in enumerate(str1):
		mat[i][mapper[c]] += 1
	for i, c in enumerate(str2):
		mat[i][mapper[c]] += 1
	return mat

strA = "AAAG"
strB = "AACG"

def getMotifInstance(str1, mat, length):
	bestScore = 0;
	bestIndex = 0;
	newScore = 0;
	for i in range(0, len(str1)):
		newScore = getScore(str1[i:i+length], mat)
		if newScore > bestScore:
			bestScore = newScore
			bestIndex = i
	return str1[bestIndex:bestIndex+length]

def getScore(str1, mat):
	score = 0
	for i, c in enumerate(str1):
		print mat, i, c, mapper, str1
		score += mat[i][mapper[c]]
	return score

def adjustMatrix(str1, mat):
	for i, c in enumerate(str1):
		mat[i][mapper[c]] += 1	

def getMotifMatrix(sequences, length):
	motif1, motif2 = getBestSubstringPair(sequences[0], sequences[1], length)
	matr = getScoreMatrix(motif1, motif2, length)
	for i in range(2, len(sequences)):
		motifN = getMotifInstance(sequences[i], matr, length)
		matr = adjustMatrix(motifN, matr)

	return matr
	

globalLength = int(open(sys.argv[2]).read())
sequences = getSequences()

getMotifMatrix(sequences, globalLength)

