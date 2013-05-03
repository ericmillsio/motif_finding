import cProfile, pstats, io
import algorithm

def run():
	pr = cProfile.Profile()
	pr.enable()

	algorithm.main(["sequences.fa","motiflength.txt"])

	pr.disable()
	s = io.FileIO("results.txt", mode='w', closefd=True)
	ps = pstats.Stats(pr, stream=s)
	ps.print_stats()
	
	time = ps.total_tt
	print time
	# time = 0.0
	# with open("results.txt","r") as filein:
	# 	arr = filein.readline().split()
	# 	i = arr.index("CPU")
	# 	time = arr[i-1]
		
	return time

if __name__ == "__main__":
	run()
