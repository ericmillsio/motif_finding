#!/usr/bin/python

import sys, random
from pyfasta import Fasta


def main(argv):
   try:
      fasta, word = argv
      s1 = Fasta(fasta)
      seq = s1[s1.keys()[0]]
      if len(word) > 10:
         raise Exception
   except Exception:
      print "Invalid input, follow rules below:"
      print "word must be 10 characters or less"
      print 'testsig.py <fastafilename> <word>'
      sys.exit(2)

   seq = [x for x in seq]
   length = len(seq)

   word = [x for x in word]
   N = wordFreq(seq, word)
   
   permutes = getPermutes(seq, word)
   #permutes = [(''.join(s[0]), s[1]) for s in permutes]
   pval = 0
   for p in permutes:
      if p[1] >= N:
         pval+=1
   pval = (pval * 1.0) / len(permutes)
   print length, N, pval

   sys.exit()

def wordFreq(seq, word):
   count = 0
   for idx, c in enumerate(seq):
      if seq[idx:idx+len(word)] == word:
         count+=1
   return count

def getPermutes(seq, word):
   lis = []
   for i in range(1000):
      random.shuffle(seq)
      count = wordFreq(seq, word)
      lis.append((list(seq),count))
   return lis


if __name__ == "__main__":
   main(sys.argv[1:])