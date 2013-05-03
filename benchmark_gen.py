#!/usr/bin/python

import sys, os, random
import benchmark as bm

icpcs = [1,1.5,2]
mls = [6,7,8]
scs = [5,10,20]

DEF_ICPC = 2
DEF_ML = 8
DEF_SC = 10
DEF_SL = 50

root = os.getcwd()

def main(argv):

    mk_dir("icpc")
    mk_dir("ml")
    mk_dir("sc")

    for i, k in enumerate(icpcs):
        run_10("icpc", k, DEF_ML, DEF_SL, DEF_SC, i*10)

    for i, k in enumerate(mls):
        run_10("ml", DEF_ICPC, k, DEF_SL, DEF_SC, i*10)

    for i, k in enumerate(scs):
        run_10("sc", DEF_ICPC, DEF_ML, DEF_SL, k, i*10)

def run_10(folder, icpc, ml, sl, sc, s_i):
    for i in range(s_i, s_i+10):
        d = root + "/" + folder + "/" + str(i)
        if not os.path.exists(d):
            os.mkdir(d)
        os.chdir(d)

        with open('details.txt', 'w') as f:
            f.write(str(icpc) + "\t" + str(ml) + "\t" + str(sl) + "\t" + str(sc) + "\n")

        bm.main([icpc, ml, sl, sc])

def mk_dir(foldername):
    d = root + "/" + foldername
    if not os.path.exists(d):
            os.mkdir(d)

if __name__ == "__main__":
   main(sys.argv[1:])