all:	
	@echo "--------------------------- Making hadoop jar file"
	hadoop com.sun.tools.javac.Main WordCount.java
	jar cf wc.jar WordCount*.class

run:	
	hadoop fs -rm -r /user/robert/wordcount/output	
	@echo "--------------------------- Running map reduce wordcount"
	hadoop jar wc.jar WordCount /user/robert/wordcount/input /user/robert/wordcount/output
	@echo "--------------------------- Checking output"
	hadoop fs -cat /user/robert/wordcount/output/part-00000
