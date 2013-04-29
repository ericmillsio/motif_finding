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
   # print seqs
   motif = gen_motif(icpc, ml)
   # print motif
   samples = [sample_motif(motif) for i in range(sc)]

   seqs = [plant(seq, samp) for samp, seq in  zip(samples, seqs)]

   with open('sequences.fa', 'w') as f:
      for i, s in enumerate(seqs):
         f.write(">seq" + str(i) + "\n" + ''.join(s[0]) + "\n")

   with open('sites.txt', 'w') as f:
      for i, s in enumerate(seqs):
         f.write("seq" + str(i) + "\t" + str(s[1]) + "\n")

   with open('motif.txt', 'w') as f:
      f.write(">MOTIF1" + "\t" + str(ml) + "\n")
      for i, s in enumerate(motif):
         for x in s[0]:
            f.write(str(x) + "\t")
         f.write("\n")

   with open('motiflength.txt', 'w') as f:
      f.write(str(ml))

   sys.exit()


def plant(seq, site):
   pos = random.randint(0, len(seq)-len(site)-1)
   for i, seed in enumerate(site):
      seq[pos+i] = seed
   return (seq, pos)


def gen_motif(icpc, ml):
   motif = []
   for x in range(ml):
      found_one = False
      while not found_one:
         # generate random row
         col = np.random.uniform(100000000,size=(1,4))
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
      sample.append( select_from_distrib(col[0].tolist()) )
   return sample

def select_from_distrib(distrib):
   poss = random.random()
   curr = 0
   for i, letter in enumerate(distrib):
      curr += letter
      if poss <= curr:
         return nuc[i]
   return nuc[3]

def info_content(col, bg, icpc):
   ic = 0
   for n in col[0]:
      ic += n * math.log(n/bg)
   return ic, icpc-0.2 <= ic <= icpc+0.2
      
def gen_seq(sl):
   seq = []
   for x in range(sl):
      seq.append(nuc[random.randint(0, 3)])
   return seq

if __name__ == "__main__":
   main(sys.argv[1:])