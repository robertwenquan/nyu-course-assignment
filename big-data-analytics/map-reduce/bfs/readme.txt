
== What is this?
 * This is the extra credit map-reduce assignment for Big Data Analytics course in Spring 2015 semester
 * by Professor Juan C Rodriguez
 * due date is Mar 10 2015

== Who made this?
 * Robert Wen (robert.wen@nyu.edu)
 * Computer Science Department of NYU Polytechnic School of Engineering
 * N12246277, NetID: qw476

== What does this assignment do?
 * This is a BFS search algorithm implemented in iterative map-reduce way.
 * The raw data is the Foursquare friendship network crawled in December 2010 by Fred Morstatter. It's public available for download at http://socialcomputing.asu.edu/datasets/Foursquare
 * This assignment works on this data, produces the relative distances from the user-id(1) to all other user-id
 * After the processing, the distances from all other users to user-id(1) will be available for direct consumption

== How does the program work?
 * The Map-reduce jobs are written in Python, which will work with Hadoop STREAMING
 * It works in an iterative way to generate the final result.
 * For this dataset, 16 iterations will be needed
 * In each iteration, it walks one-level deeper into the graph. The node visited will be marked as "DONE". Its children will be marked as "TODO", and distance as parent's distance plus one.
 * After each iteration of the mapper, there might be redundant user-id information as different users may have the same friend. The reducer will eliminate all the duplicated user IDs and leave only one with the least distance from the root
 * Finally, once there is no user-id under "WAIT" or "TODO" state, the job is done
 * NOTE: You may notice the number of "WAIT" and "TODO" nodes are growing initially. That is because more user IDs are discovered from the friends map. And those user IDs are not initially in the raw data. Those user IDs will be only some others' friends but don't have any friend under them. After growing in a few iterations, eventually the number of "WAIT" and "TODO" nodes will converge to ZERO

== The Raw Data Format
 * The raw data is fetched and stored under data/edges.csv
 * Each line contains one relationship between two user-id, separated by comma
 * Sample data: "100000,100950"

== The Input Data Format
 * For the convenience of processing in map-reduce, we pre-preocess the raw data into a format that is convenient to process
 * Each line contains the following information
 ** User ID
 ** All friends as a list, separated by comma. This could be empty, meaning the user has no friend.
 ** Distance to the root(user-id 1). If it's the user-id 1, distance is 0. By default the distance is all set to -1, meaning infinite or unknown
 ** State of this user(WAIT,TODO,DONE)
 *** WAIT means this node is not processed. And there is not enough information to process this node yet.
 *** TODO means there is enough enough information to process this node. This node will be processed in the next iteration of map-reduce job.
 *** DONE means this node has been processed and will never be processed again.
 ** Parent user id. If it's the root node, parent is set to "root". By default the user id is set to "na", meaning "not available".
 * Sample data: "100208  101656,104452,106224,212015,212016,212017,48148,67000,76518,87897,90138,91659|-1|WAIT|na"

== The Final Data Format
 * It's in the same format of the input file. But all nodes should be in "DONE" state.
 * And all nodes should have a distance relative to the root node
 * And all nodes should have a parent node number
 * Sample data: "72179 100950,105585,106224,143249,57265,63502,76518,85450,85608,87185,88601,90013,91659|7|DONE|90013"

== Environment
 * In order for this map-reduce to run, I assume GNU make, awk, bash, python and of course hadoop are all installed properly
 * Here is the software version I am using, just FYI
 ** bash 4.3.11
 ** Python 2.7.6
 ** Awk 4.0.1
 ** GNU make 3.81
 ** hadoop 2.6.0 

== How to run?
 * Here are the steps to run the map-reduce job

 # This will clean all the output files in output directory
  $ make clean

 # This will do the following
 # 1. convert raw data file into desired input format
 # 2. make a clean HDFS directory under /user/robert/bfs
 # 3. make HDFS /user/robert/bfs/input and upload the initial input data into it
  $ make prepare

 # This will dry-run the map-reduce python scripts without the HADOOP
 # in the same iterative way as it does in HADOOP
 # output files will be generated under output/output.*
  $ make dryrun

 # This will run the map-reduce job with HADOOP STREAMING
 # The same Python scripts will be run, but in the HADOOP environment
  $ make run

== How to check the results?
 * Check the HDFS output
  $ hadoop fs -ls /user/robert/bfs/

 * Check the local output
  $ ls -l output/

