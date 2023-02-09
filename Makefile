
# list files to be compiled in comp target

comp:
	rustc run.rs

run: comp
	# temporarily just run. run will need commandline arguments
	./run

delete_everything:
	rm -R API Brain Metricizer Output ReadWrite Scorer 
