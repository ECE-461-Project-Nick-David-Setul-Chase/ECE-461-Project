
# list files to be compiled in comp target

comp:
	rustc run.rs

run: comp
	./run build
	./run practice_url_file.delete_me
	./run test

delete_everything:
	rm -R API Brain Metricizer Output ReadWrite Scorer 
