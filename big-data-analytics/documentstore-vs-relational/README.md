## DocumentStore vs Relational Store A comparative Analysis
#### a comparative analysis of MySQL and mongo as dataStores

This paper is a course assignment for the Big Data Analytics class in Spring 2015 semester<br>
Robert Wen (robert.wen@nyu.edu), N12246277, NetID: qw476<br>

#### Introduction

This paper is a comparative analysis between SQL and noSQL database. Specifically we choose MySQL and MongoDB as a representative of each database category for the analysis. First we illustrate the conceptual and syntactical difference for the common data store/query manipulations. Beyond that, we also perform a series of performance experiments to reveal the performance difference between the two databases. It is assumed the reader has moderate knowledge on both MySQL and MongoDB because we don't cover any fundamentals of those two databases but directly dive into the comparison of them.

#### Conceptual Comparison

First let's compare the conceptual terminology between MySQL and MongoDB

| MySQL           |  MongoDB            |
| --------------- | ------------------- |
| Database        |  Database           |
| Table           |  Collection         |
| Row             |  Document           |
| Column          |  Field              |
| Table Join      |  Embedded Documents |
| mysqld(server)  |  mongod             |
| mysql(client)   |  mongo              |

The major difference between SQL and noSQL database is the name of table and row. Instead of calling table and row in the SQL databases, a.k.a. RDBMS, "Collection" and "Document" are used. In SQL database context, we say there are a bunch of rows in the table and a few tables in that database. In the noSQL database context, we say there are a few documents in this collection and a few collections of documents in that database.

#### Syntactic Comparison

Then let's compare the grammar of some common data retrieval tasks from SQL and noSQL for the common tasks like creating database, creating table, inserting a row, select rows, deleting rows, table or database.

###### For SQL: 

* Create database: CREATE DATABASE DBNAME; USE DBNAME;
* Create Table: CREATE TABLE TABLENAME (column_name1 type1, column_name2 type2);
* Add Record: INSERT into TABLENAME (column_name1, column_name2) VALUES(value1, value2);
* Select Record: SELECT column_name1, column_name2 from TABLENAME;
* Update Record: UPDATE TABLENAME set column_name1 = value1 WHERE column_name5 == 'Jacky';
* Delete Record: DELETE from TABLENAME where column_name4 == "NA";
* Delete Table:  DROP TABLE TABLENAME;
* Delete Database: DROP DATABASE DBNAME;

###### For noSQL:

* Create Database: use DBNAME
* Create Table: Not necessary. (When the first record is inserted. The table is created.)
* Add Record: db.TABLENAME.insert(JSON_STRING)
* Select Record: db.TABLENAME.find({}, {_id:0})
* Delete Record: db.TABLENAME.remove(SELECTION_CRITERIA)
* Update Record: db.TABLENAME.update(SELECTION_CRITERIA, UPDATE_DATA)
* Delete Table: db.TABLENAME.drop()
* Delete Database: db.dropDatabase()

Syntactically, SQL is more readable because it's more close to the natural language statement. You state what you want to do with the SQL and you get what you want. For the noSQL query in MongoDB, things like {}, and ":", and the "." connecting the data collection and the method name, makes the query language more like a programming language rathan than a data query statement. For people with background of JSON it might be familiar but for people we don't there will be some leaning curve.

#### Comparison of capabilities available in both

As for common capabilities, both SQL and noSQL databases have the following features:

* Add, Query, Update and Delete
* data import and export
* CLI manipulation of the data
* Programmable APIs for various programming languages
* Server / Client model

#### Limitations of SQL Engines

Although traditional SQL databases have evoled several decades and have dominated the database market, it still has several limitations. Those limitations are also the motive to create the noSQL databases.

* Relational database has scalability concern. While SQL databases have better vertical scalability than noSQL databases, the scaling trend is not linear when the computing resource doulbes more than twice.
* Fixed schema. Everything has to be converted into table schema. Not good for unstructural data. 
* Hierarchical data.
 
#### Limitations of Document Stores 

Depiste of the booming of noSQL databases in the recent years, it does not mean we should abandom the traditional SQL database and all switch to adopt the noSQL databases. Because noSQL database may not fit all environment. Here are a few limitations about the noSQL databases:

* NoSQL DB is not doing well on complex queries
* No unified query language. Every vendor has its own query convention.
* For high transactional based application. NoSQL is not stable enough.
* Lack of commercial support. 
* Data Integrity
* Not easy to join table
 
#### Experimental environment 

The following experimental analysis is based on the MySQL and MongoDB instances sponsored by IBM. 

Here is the basic hardware configuration of those two database hosts:

Host  | IP Address    | CPU                    | Memory                |   Disk   
----- | ------------- | ---------------------- | --------------------- | --------------------
mysql | 174.79.32.150 | POWER7 3.3 GHz 80 lcpu | 30 GB                 | 1000 GB
mongo | 174.79.32.135 | POWER7 3.3 GHz 32 lcpu | 30 GB(cross numa-node)| 200 GB backed by LVM

As we can see from the above, they are two POWER7 machines with equivalent amount of memory but different number of logical CPUs. That is to say the host running MySQL is much more powerful than the other running MongoDB. Also the MySQL host has 5x disk space than the MongoDB one. 

The number of logical CPUs will affect the overall throughput of the database but as all of my test cases are all single threaded, we can assume there is no performance difference between those two hosts because the single core frequency is the same across the two nodes. In a more series test, we will need to avoid this kind of mismatch on the hardware configuration. 

For the mismatch of the disk size, as my test cases do not utilize much disk space, we can assume there is no impact on the differnece of the disk space. 

The other notable glitch on the mongoDB node is that the memory is not well configured. Somehow there are two NUMA nodes on this host but there is no local memory attached to the NUMA node0. This will lead to cross-node memory access, with much higher memory latency than the local memory access. This will definitely affect the performance for all applications running on this host. As it's a homework assignment, I am going to ignore this but in a real world testing, this must be correct in order to make the test result legitimate.

#### Experimental Data

The data for this experiment is the Flickr image meta data provided by Yahoo Labs
http://webscope.sandbox.yahoo.com/catalog.php?datatype=i&did=67

The original data is 100 million items. For this experiment, we only extract 1 million items from it.

The input data format after initial filtering and processing is like this. We have 1 million items in this format.
```
{
 u'image_urls': [u'https://38.media.tumblr.com/65e7f3f16c4036812e60a348f8c67974/tumblr_nm0ge7TmRk1ur4qc3o2_250.gif'],
 u'labels': [],
 u'ref_urls': [u'http://tmblr.co/ZJOTLv1h90ouq'],
 u'tumblr_blogurl': u'http://seethesunlight3.tumblr.com/',
 u'tumblr_notes': 260,
 u'tumblr_timestamp': 1427735583,
 u'url': u'https://38.media.tumblr.com/65e7f3f16c4036812e60a348f8c67974/tumblr_nm0ge7TmRk1ur4qc3o2_250.gif'
}
```

To process the input data format in MySQL and MongoDB, we need some data format transformation. Generally for MySQL we only extract the fileds of our interest and save the fileds into a table. For MongoDB because of its native support of JSON, we simply import the whole JSON object into the data collection.

The following table schema is used for MySQL, to store the extracted data fields from the raw input JSON format.
```
mysql> desc flickr_pics;
+-----------+--------------+------+-----+---------+-------+
| Field     | Type         | Null | Key | Default | Extra |
+-----------+--------------+------+-----+---------+-------+
| timestamp | mediumtext   | YES  |     | NULL    |       |
| imgurl    | varchar(256) | YES  |     | NULL    |       |
| blogurl   | varchar(256) | YES  |     | NULL    |       |
| labels    | varchar(512) | YES  |     | NULL    |       |
+-----------+--------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

#### Time to INSERT "n" records

In this experiment, we do the comparative analysis for record insertion into mysql and mongodb.
In order to see a better trend of how they work with various volumns, I choose a series of numbers from 100 to 1 million.
For each experiment, we clear the whole database and only insert those number of records.

* For MySQL1, we use SQL to import each of the record
* For MySQL2, we use import command to import all records in one batch
* For MySQL3, we accumulate the data transformation time from JSON to TSV as MySQL does not support JSON import
* For MongoDB1, we use db.table.insert() to import each of the record
* For MongoDB2, we use mongoimport to import all records in one batch

(INSERT) |   100  |   1000  |   10000 |   100000    |   1000000
-------- | ------ | ------- | ------- | ----------- | ------------
MySQL1   | 1.346  | 12.485  | 126.883 | 1300.000(*) | 13000.000(*)
MySQL2   | 0.138  |  0.355  |  1.194  |    3.995    |    31.317
MySQL3   | 0.188  |  0.680  |  4.293  |   35.307    |   344.560
MongoDB1 | 0.151  |  1.055  | 10.642  |  106.379    |  1060.000(*)
MongoDB2 | 0.026  |  0.086  |  0.674  |    6.685    |    68.959

(*) Not tested but projected value

![INSERT Performance Comparison](images/plot-insert.png)

From the above we can observe it is very unwise to load data via SQL INSERT. Even if we haven't experimented the 100000 records, it is expected to load the data in several hours, which is unbearable. The MySQL2 measurement looks the most promising among all the insertion means, but it is without the pre-processing of the raw data. Remember our raw data is in JSON format, we need to pre-process it in order to be imported by MySQL. The MySQL3 measurement is with the additional data pre-processing time, which seems not that promising compared to the numbers in MongoDB2 measurement.

Despite of the native support of JSON on MongoDB, we still try the per-record insertion with MongoDB. It is not surprising to see it's much slower in MongoDB1 than MongoDB2. But it's not that slow compared to the MySQL1 measurement. For 1 million records, it is anticipated to be loaded in less than 20 minutes. In the faster single batch import in Mongo, it outperforms MySQL by aggregated data processing time, but it is still about 2 times slower than MySQL considering about the data import separately. So if it's not JSON format but it's CSV format which MySQL could handle, it might be more efficient in MySQL for the data import.

#### Time to SELECT "n" records

In this experiment, we would like to see how many distinct blogs are in the dataset. 

For MySQL, we use SELECT DISTINCT to query distinct records 
```
> MySQL1: SELECT DISTINCT blogurl from flickr_pics;
> MySQL2: SELECT COUNT(DISTINCT blogurl) from flickr_pics;
```
For MongoDB, we use db.collection.distinct() to query the distinct records
```
> MongoDB1: db.flickr_pics.distinct("tumblr_blogurl")
> MongoDB2: db.flickr_pics.aggregate
            (
              {
                $group : {_id : "$tumblr_blogurl"} 
              }, 
              {
                $group : {_id : 1, count: {$sum : 1}}
              }
            )
```

(SELECT) |   100  |  1000  | 10000  | 100000  | 1000000
-------- | ------ | ------ | ------ | ------- | --------
MySQL1   | 0.019  | 0.031  | 0.464  |  3.084  |  29.839
MySQL2   | 0.005  | 0.007  | 0.026  |  0.269  |   3.281
MongoDB1 | 0.042  | 0.050  | 0.130  |  0.837  |   6.180
MongoDB2 | 0.037  | 0.040  | 0.066  |  0.322  |   2.822

As we can see from the plot, for both queries MySQL performs better than MongoDB in smaller dataset. When the dataset goes bigger, the query1 from MySQL does much worse than MongoDB. But for the query2, only when the dataset goes up to 1 million the performance on MySQL is defeated by MongoDB to a small extent. From the syntactical point of view, both queries in MySQL is straight-forward to understand. The first query for MongoDB is also good in understanding level. But the second query in MongoDB is really a bit tedious from understanding point of view or typing effort point of view.

![SELECT Performance Comparison](images/plot-select.png)

#### Time to UPDATE "n" records

In this experiment, we modify the blogurl data field in the table for all data records. The original data for the blogurl is like "http://myblogname.tumblr.com/". We would like to strip the leading "http://" and the trailing "/" for the blogurl and have it as "myblogname.tumblr.com".

For MySQL, we use the following SQL query:
```
> UPDATE flickr_pics SET blogurl = REPLACE(REPLACE(blogurl, 'http://', ''),'/','');
```

For MongoDB, we use the following MongoDB query:
```
> db.flickr_pics.find().forEach(
    function(u) {
      u.tumblr_blogurl = u.tumblr_blogurl.replace(/http\:\/\//g, "").replace(/\//, "");
      db.flickr_pics.save(u); }
    );
```

(UPDATE)|   100 |  1000 | 10000 | 100000  | 1000000 |
------- | ----- | ----- | ----- | ------- | ------- |
MySQL   | 0.019 | 0.031 | 0.464 |  3.084  |  29.839 |
MongoDB | 0.066 | 0.311 | 2.916 | 27.525  | 274.375 |

![INSERT Performance Comparison](images/plot-update.png)

From the above we can observe the update performance on MySQL is much superior than that of MongoDB. That is because Mongo DB does not have native support for string replacement manipulation in UPDATE query. Instead we have to iterate each data record and set the value back.

We can also observe the performance scales linearly on the data scale, both on MySQL and MongoDB. So in the real environment we can do some small dataset as performance evaluation and estimate the actual time cost of a bigger set. 

#### Time to DELETE "n" records

In this experiment, we try to delete the records/documents from the table/collection. In MySQL there is DELETE statement and TRUNCATE statement to do the same task so we experiment on both of them. 

* MySQL1 is using DELETE from TABLENAME to delete all records from the table.
* MySQL2 is using TRUNCATE TABLE TABLENAME to truncate the table to empty.
* MongoDB is using db.TABLENAME.drop() to drop the collection(table).

(DELETE)|   100  | 1000    | 10000   | 100000   |1000000
------- | ------ | ------- | ------- | -------- | ------
MySQL1  | 0.018  | 0.018   | 0.281   | 1.099    | 14.906
MySQL2  | 0.078  | 0.072   | 0.215   | 0.108    |  0.275
MongoDB | 0.036  | 0.035   | 0.036   | 0.036    |  0.036

![INSERT Performance Comparison](images/plot-delete.png)

From the above performance data, we can see the DELETE query from MySQL is a O(n) while the TRUNCATE from MySQL and db.TABLE.drop() from MongoDB are both O(1). So when we delete table, we never want to use "DELETE from TABLE" to delete a table from MySQL when the table is considerably large.

#### Time to process rich variety

In this experiment, we are going to execute a bunch of queries on MySQL and MongoDB 1/5 times and compare the runtime on those aggregated tasks.

On MySQL we are going to execute:
```
SELECT * FROM flickr_pics LIMIT 30;
SELECT timestamp, labels FROM flickr_pics LIMIT 20;
SELECT imgurl, labels FROM flickr_pics WHERE timestamp > 1427735965 AND timestamp < 1427735988 LIMIT 30;
SELECT COUNT(DISTINCT blogurl) FROM flickr_pics;
```

On MongoDB we are going to execute:
```
db.flickr_pics.find().limit(30)
db.flickr_pics.find( {},{_id:0, tumblr_timestamp:1, labels:1} ).limit(20)
db.flickr_pics.find( {tumblr_timestamp :{$gt: 1427735965, $lt: 1427735988}},{_id:0, url:1, labels:1} ).limit(30)
db.flickr_pics.aggregate ( { $group : {_id : "$tumblr_blogurl"} }, { $group : {_id : 1, count: {$sum : 1}} } )
```

* MySQL1: Execute the above MySQL commands one time
* MySQL2: Execute the above MySQL commands five times
* MongoDB1: Execute the above MongoDB commands one time
* MongoDB2: Execute the above MongoDB commands five times

(VARIATY)|    100  |   1000  |  10000  | 100000  |1000000
-------- | ------- | ------- |  ------ | ------- | ------
MySQL1   |  0.006  |  0.008  |  0.024  |  0.274  |  4.887
MySQL2   |  0.012  |  0.019  |  0.103  |  1.603  | 16.002
MongoDB1 |  0.063  |  0.065  |  0.093  |  0.357  |  2.808
MongoDB2 |  0.143  |  0.157  |  0.284  |  1.553  | 13.851

![Variety Performance Comparison](images/plot-variaty.png)

Similarly, MySQL does better on smaller dataset. But when dataset goes to 1 million, MongoDB outperforms. It is believed MongoDB will outperform even more significant when the dataset goes even larger to web scale, because we haven't scaled the workload horizontally to multiple database nodes yet. 

#### Conclusions

As from the comparative analysis from the above experiments, we can clearly see it is hard to draw a conclusion whether SQL or noSQL is better than the other. For most experiments, it works more efficient on MySQL with small dataset but vice versa. In some other experiments, MongoDB performs constantly better than MySQL. For complex queries it is usually more handy to write the SQL statements to perform the task while keeping good readability of the query language, but MongoDB might perform better with larger dataset even if the query statement is as complex as a short script. Generally MongDB does well on insertion, selection and deletion, but it does not perform well on update. 

#### TODO for this analysis

Although we already have done fair amount of performance analysis against those two databases, there is still large gap to fill to understand the performance between those two databases. The first thing is for really complex queries. Due to the time constraint, we haven't constructed page long SQL statement to stress the MySQL. Also when we have a page long SQL query statement, it is very hard to "translate" it to equivalent MongoDB query string. The other big point we have ignored is the web scale data. MongoBD is really good at scaling horizontally, and it does not make sense if we scale it to multiple nodes without several hundred million large dataset. Although we haven't tried. The 1 million dataset has already shown the non-trivial performance advantage over MySQL in some queries. It is anticipated to gain more benefit when the dataset grows to a web scale. But still more experiments need to be performed in order to understand this different from a quantity point of view.

#### Reference

* http://www.thegeekstuff.com/2014/01/sql-vs-nosql-db/
* http://www.mongodb.com/nosql-explained
* http://www.scriptrock.com/articles/mysql-vs-mongodb
* http://www.tutorialspoint.com/mongodb/index.htm

