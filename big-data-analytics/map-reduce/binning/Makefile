all:	
	@echo "--------------------------- Making hadoop jar file"
	hadoop com.sun.tools.javac.Main WordCountBinning.java
	jar cf wc.jar WordCountBinning*.class
	hadoop fs -mkdir /user/robert/wordcount-binning/output

prepare:	
	hadoop fs -mkdir /user/robert/wordcount-binning
	hadoop fs -mkdir /user/robert/wordcount-binning/input
	hadoop fs -mkdir /user/robert/wordcount-binning/output
	hadoop fs -copyFromLocal input/* /user/robert/wordcount-binning/input/

run:	
	hadoop fs -rm -r /user/robert/wordcount-binning/output	
	@echo "--------------------------- Running map reduce wordcount-binning"
	hadoop jar wc.jar WordCountBinning /user/robert/wordcount-binning/input /user/robert/wordcount-binning/output
	@echo "--------------------------- Checking output"
	hadoop fs -ls /user/robert/wordcount-binning/output/

clean:	
	@rm -f *.class *.jar

cleanall:	clean
	@hadoop fs -rm -r /user/robert/wordcount-binning
