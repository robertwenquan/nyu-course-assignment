# Big Data Analytics Spring 2015
#### Assignment for Hadoop MapReduce Binning (Due Mar 8 2015)
###### Robert Wen (robert.wen@nyu.edu)
###### N12246277, NetID: qw476

### Instructions to run the Map-Reduce application
```
$ make prepare
$ make
$ make run
```

### Sample output for this application
```
hadoop fs -ls /user/robert/wordcount-binning/output/
15/03/07 11:43:11 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Found 5 items
drwxr-xr-x   - hduser supergroup          0 2015-03-07 11:43 /user/robert/wordcount-binning/output/10
drwxr-xr-x   - hduser supergroup          0 2015-03-07 11:43 /user/robert/wordcount-binning/output/100
drwxr-xr-x   - hduser supergroup          0 2015-03-07 11:43 /user/robert/wordcount-binning/output/1000
drwxr-xr-x   - hduser supergroup          0 2015-03-07 11:43 /user/robert/wordcount-binning/output/10000
-rw-r--r--   1 hduser supergroup          0 2015-03-07 11:43 /user/robert/wordcount-binning/output/_SUCCESS
hadoop fs -ls /user/robert/wordcount-binning/output/10/
15/03/07 11:43:16 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Found 1 items
-rw-r--r--   1 hduser supergroup      99863 2015-03-07 11:43 /user/robert/wordcount-binning/output/10/part-00000
hadoop fs -ls /user/robert/wordcount-binning/output/100/
15/03/07 11:43:21 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Found 1 items
-rw-r--r--   1 hduser supergroup       4236 2015-03-07 11:43 /user/robert/wordcount-binning/output/100/part-00000
hadoop fs -ls /user/robert/wordcount-binning/output/1000/
15/03/07 11:43:27 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Found 1 items
-rw-r--r--   1 hduser supergroup        426 2015-03-07 11:43 /user/robert/wordcount-binning/output/1000/part-00000
hadoop fs -ls /user/robert/wordcount-binning/output/10000/
15/03/07 11:43:32 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Found 1 items
-rw-r--r--   1 hduser supergroup         41 2015-03-07 11:43 /user/robert/wordcount-binning/output/10000/part-00000

```
