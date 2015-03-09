
prepare:	
	./generate-data.awk < data/edges.csv > input/relation.map
	hadoop fs -rm -r -f /user/robert/bfs
	hadoop fs -mkdir -p /user/robert/bfs/input
	hadoop fs -copyFromLocal input/relation.map /user/robert/bfs/input/

run:	
	./mr-iterative.sh

dryrun:
	./iterative.sh

clean:	
	rm -f output/part* output/output*

