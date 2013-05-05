import sys
import numpy, math
from heapq import heappush, heapreplace

mapper = { 'A': 0, 'C': 1, 'T': 3, 'G': 2}
revMapper = {  0:'A',  1:'C',  3:'T' ,  2:'G'}

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
    for i in range(len(str1)-length):
        newScore = getScore(str1[i:i+length], mat)
        if newScore > bestScore:
            bestScore = newScore
            bestIndex = i
    return str1[bestIndex:bestIndex+length], bestIndex

def getScore(str1, mat):
    #sums = mat.sum()
    #norm = (1*matr).astype(float)
    #norm /= norm.sum()
    #norm += 0.00001
    score = 1
    for i, c in enumerate(str1):
        score *= mat[i][mapper[c]]
    return score

def adjustMatrix(str1, mat):
    for i, c in enumerate(str1):
        mat[i][mapper[c]] += 1  

def getIC(matr):
    summer = 0.0
    for i in matr:
        summer += info_content(i, 0.25)
    return summer
    
def info_content(col, bg):
   ic = 0.0
   for n in col:
        ic += n * math.log(n/bg, 2)
   return ic

def getNormalizedMatrix(matr):
    norm = (1*matr).astype(float)
    # normalize
    for i in norm:
        i += 0.05
        i /= i.sum()
    return norm

def getMotifMatrix(seqs, length, numSpread):

    heaped = []
    for i in range(0, len(seqs[0])-length):
        for j in range(0, len(seqs[1])-length):
            newScore = hammingDistance(seqs[0],i, seqs[1], j, length)
            
            if numSpread > 0 :
                heappush(heaped, (newScore, i, j))
                numSpread -= 1
            elif heaped[0][0] < newScore:
                heapreplace(heaped, (newScore,i,j))
    #this lines is dope
    matricies = [ getScoreMatrix(seqs[0][ q[1]:q[1]+length ], seqs[1][ q[2]:q[2]+length ], length) for q in heaped]     

    bestSites = {}
    bestMatrix = []
    bestIC = 0
    bestIndex = 0
    for i, M in enumerate(matricies) :
        sites = {}
        
        for j,s in enumerate(seqs[2:]) :
            norm = getNormalizedMatrix(M)         
            str1, bestIndex = getMotifInstance(s, norm, length)
            sites[j+2] = bestIndex
            adjustMatrix(str1, M)
   
        newIC = getIC( getNormalizedMatrix(M) )
        if newIC > bestIC :
            bestSites = sites
            bestMatrix = M
            bestIC = newIC
            bestIndex = i



    bestSites[0] = getMotifInstance(seqs[0], getNormalizedMatrix(bestMatrix), length)[1]
    bestSites[1] = getMotifInstance(seqs[1], getNormalizedMatrix(bestMatrix), length)[1]
    
    return bestMatrix, bestSites
    
def main(argv):
    globalLength = int(open(argv[1]).read())
    sequences = getSequencesFromFile(argv[0])
    matter, sites =  getMotifMatrix(sequences, globalLength, 500)
    # print " ",["A","C","G","T"]
    
    # #FOR PRINTING OUTPUT IF RUNNING JUST THIS
    # print matter
    # for i in matter.argmax(1):
    #     print revMapper[i]


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
    

