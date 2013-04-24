#!/usr/bin/python

import sys, random
from pyfasta import Fasta
import numpy as np


nuc = ['A', 'C', 'G', 'T']

def main(argv):
   try:
      icpc, ml, sl, sc = argv

   except Exception:
      print "Invalid input, follow rules below:"
      print "word must be 10 characters or less"
      print 'testsig.py <fastafilename> <word>'
      sys.exit(2)

   print gen_seq(int(sl))

   sys.exit()


def gen_motif(icpc, ml):
   A=np.random.randint(4,size=(ml,4))

def gen_seq(sl):
   seq = ""
   for x in range(sl):
      seq += nuc[random.randint(0, 3)]
   return seq

if __name__ == "__main__":
   main(sys.argv[1:])