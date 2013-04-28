#!/usr/bin/python

import sys, random, math
from pyfasta import Fasta
import numpy as np


nuc = ['A', 'C', 'G', 'T']

def main(argv):
   try:
      icpc, ml, sl, sc = argv
      icpc, ml, sl, sc = float(icpc), int(ml), int(sl), int(sc)

   except Exception:
      print "Invalid input, follow rules below:"
      sys.exit(2)

   seqs = [gen_seq(sl) for i in range(sc)]
   print seqs
   motif = gen_motif(icpc, ml)
   print motif
   sample_motif(motif)
   sys.exit()


def gen_motif(icpc, ml):
   motif = []
   for x in range(ml):
      found_one = False
      while not found_one:
         # generate random row
         col = np.random.uniform(100,size=(1,4))
         # normalize
         col /= col.sum()
         ic, within_rng = info_content(col, 0.25, icpc)
         if within_rng:
            motif.append(col)
            found_one = True
   return motif

def sample_motif(motif):
   sample = []
   for col in motif:
      poss = random.random()
      curr = 0
      for i, letter in enumerate(col):
         print letter
         if poss <= letter:
            sample.append(nuc)
            break;
         curr += letter
   print sample

def info_content(col, bg, icpc):
   ic = 0
   for n in col[0]:
      ic += n * math.log(n/bg)
   return ic, icpc-0.2 <= ic <= icpc+0.2
      
def gen_seq(sl):
   seq = ""
   for x in range(sl):
      seq += nuc[random.randint(0, 3)]
   return seq

if __name__ == "__main__":
   main(sys.argv[1:])