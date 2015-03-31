## DocumentStore vs Relational Store A comparative Analysis
#### a comparative analysis of MySQL and mongo as dataStores

This paper is a course assignment for the Big Data Analytics class in Spring 2015 semester<br>
Robert Wen (robert.wen@nyu.edu), N12246277, NetID: qw476<br>

##### Introduction

This paper is a comparative analysis between SQL and noSQL database. Specifically we choose MySQL and MongoDB as a representative of each database category for the analysis. First we illustrate the conceptual and syntactical difference for the common data store/query manipulations. Beyond that, we also perform a series of performance experiments to reveal the performance difference between the two databases.

##### Limitations of SQL Engines

Although traditional SQL databases have evoled several decades and have dominated the database market, it still has several limitations. Those limitations are also the motive to create the noSQL databases.

* Relational database has scalability concern. While SQL databases have better vertical scalability than noSQL databases, the scaling trend is not linear when the computing resource doulbes more than twice.
* Fixed schema. Everything has to be converted into table schema. Not good for unstructural data. 
* Hierarchical data.
 
##### Limitations of Document Stores 

Depiste of the booming of noSQL databases in the recent years, it does not mean we should abandom the traditional SQL database and all switch to adopt the noSQL databases. Because noSQL database may not fit all environment. Here are a few limitations about the noSQL databases:

* NoSQL DB is not doing well on complex queries
* No unified query language. Every vendor has its own query convention.
* For high transactional based application. NoSQL is not stable enough.
* Lack of commercial support. 
* Data Integrity
* Not easy to join table
 
##### Comparison of capabilities available in both

As for common capabilities, both SQL and noSQL databases have the following features:

* Add, Query, Update and Delete
* CLI manipulation of the data
* data import and export
* Programmable APIs for various programming languages

##### conceptual and syntactic ease of achieving information retrieval and manipulation tasks

First let's compare the conceptual terminology between MySQL and MongoDB

| MySQL           |  MongoDB            |
| --------------- | ------------------- |
| Database        |  Database           |
| Table           |  Collection         |
| Row             |  Document           |
| Column          |  Field              |
| Table Join      |  Embedded Documents |
| Primary Key     |  Primary Key        |
| mysqld(server)  |  mongod             |
| mysql(client)   |  mongo              |

Then let's compare the grammar of some common data retrieval tasks from SQL and noSQL for the following common tasks:

* Create database
* Create a new table
* Add a new record to a data set
* Select a few records from a data set
* Update a value of a record in a data set
* Delete a record from a data set
* Delete a table
* Delete database

For SQL: 

* Create database: CREATE DATABASE DBNAME; USE DBNAME;
* Create Table: CREATE TABLE TABLENAME (column_name1 type1, column_name2 type2);
* Add Record: INSERT into TABLENAME (column_name1, column_name2) VALUES(value1, value2);
* Select Record: SELECT column_name1, column_name2 from TABLENAME;
* Update Record: UPDATE TABLENAME set column_name1 = value1 WHERE column_name5 == 'Jacky';
* Delete Record: DELETE from TABLENAME where column_name4 == "NA";
* Delete Table:  DROP TABLE TABLENAME;
* Delete Database: DROP DATABASE DBNAME;

For noSQL:

* Create Database: use DBNAME
* Create Table: Not necessary. (When the first record is inserted. The table is created.)
* Add Record: db.TABLENAME.insert(JSON_STRING)
* Select Record: db.TABLENAME.find({}, {_id:0})
* Delete Record: db.TABLENAME.remove(SELECTION_CRITERIA)
* Update Record: db.TABLENAME.update(SELECTION_CRITERIA, UPDATE_DATA)
* Delete Table: db.TABLENAME.drop(SELECTION_CRITERIA)
* Delete Database: db.dropDatabase()

##### Experimental environment

The following experimental analysis is based on the MySQL and MongoDB instances sponsored by IBM. 

Here is the basic hardware configuration of those two database hosts:

Host  | IP Address    | CPU                    | Memory                |   Disk   
----- | ------------- | ---------------------- | --------------------- | --------------------
mysql | 174.79.32.150 | POWER7 3.3 GHz 80 lcpu | 30 GB                 | 1000 GB
mongo | 174.79.32.135 | POWER7 3.3 GHz 32 lcpu | 30 GB(cross numa-node)| 200 GB backed by LVM

##### Experimental Data

The data for this experiment is the Flickr image meta data

* img_url
* labels
* blog_url

##### time to add "n" records

Here we do the comparative experiment for record insertion into mysql and mongodb.
In order to see a better trend of how they work with various volumns, I choose a series of numbers from 100 to 1 million.
For each experiment, we clear the whole database and only insert those number of records.

For MySQL1, we use SQL to import each of the record
For MySQL2, we use import command to import all records in one batch
For MySQL3, we accumulate the data transformation time from JSON to TSV as MySQL does not support JSON import
For MongoDB1, we use db.table.insert() to import each of the record
For MongoDB2, we use mongoimport to import all records in one batch

Record
(INSERT)   100    1000    10000     100000      1000000
----------------------------------------------------------
MySQL1   1.346  12.485  126.883   1300.000(*) 13000.000(*)
MySQL2   0.138   0.355    1.194	     3.995       31.317
MySQL3   0.188   0.680    4.293     35.307      344.560
MongoDB1 0.151   1.055   10.642    106.379     1060.000(*)
MongoDB2 0.026   0.086    0.674      6.685       68.959

(*) Not tested but projected value

Plot it with line chart

Draw a conclusion based on the above observation:
Which one plays better on small dataset?
Which one plays better on large dataset?
How many records could be inserted in 1s, 1min, 1hr, 1day on MySQL and MongoDB?


##### time to process "n" rows

In this experiment, we would like to see how many distinct

For MySQL, we use SELECT DISTINCT to query distinct records 
'''
> MySQL1: SELECT DISTINCT blogurl from flickr_pics;
> MySQL2: SELECT COUNT(DISTINCT blogurl) from flickr_pics;
'''
For MongoDB, we use db.collection.distinct() to query the distinct records
'''
> MongoDB1: db.flickr_pics.distinct("tumblr_blogurl")
> MongoDB2: db.flickr_pics.distinct("tumblr_blogurl")
'''

Process 100 records
Process 1000 records
Process 10000 records
Process 100000 records
Process 1000000 records

Record
(SELECT)   100    1000     10000   100000   1000000
---------------------------------------------------
MySQL1    0.019   0.031    0.464    3.084    29.839
MySQL2    0.005   0.007    0.026    0.269     3.281
MongoDB1  0.042   0.050    0.130    0.837
MongoDB2

Plot it with line chart


##### time to update "n" records

In this experiment, we modify the blogurl data field in the table for all data records. The original data for the blogurl is like "http://myblogname.tumblr.com/". We would like to strip the leading "http://" and the trailing "/" for the blogurl and have it as "myblogname.tumblr.com".

For MySQL, we use the following SQL query:
'''
> UPDATE flickr_pics set blogname = xxxx
'''

For MongoDB, we use the following MongoDB query:
'''
> db.flickr_pics.find().forEach(
    function(u) {
      u.tumblr_blogurl = u.tumblr_blogurl.replace(/http\:\/\//g, "").replace(/\//, "");
      db.flickr_pics.save(u); }
    );
'''

Update 100 records
Update 1000 records
Update 10000 records
Update 100000 records
Update 1000000 records

Record
(UPDATE)   100    1000    10000   100000    1000000
---------------------------------------------------
MySQL    0.019   0.031    0.464    3.084     29.839
MongoDB  0.066   0.311    2.916   27.525    274.375

Plot it with line chart

From the above we can observe the update performance on MySQL is much superior than that of MongoDB. That is because Mongo DB does not have native support for string replacement manipulation in UPDATE query. Instead we have to iterate each data record and set the value back.

We can also observe the performance scales linearly on the data scale, both on MySQL and MongoDB. So in the real environment we can do some small dataset as performance evaluation and estimate the actual time cost of a bigger set. 

##### time to delete "n" records

Delete 100 records
Delete 1000 records
Delete 10000 records
Delete 100000 records
Delete 1000000 records

MySQL1 is using DELETE from TABLENAME to delete all records from the table
MySQL2 is using TRUNCATE TABLE TABLENAME to truncate the table to empty

Record
(DELETE)   100    1000    10000   100000    1000000
---------------------------------------------------
MySQL1   0.018   0.018    0.281    1.099     14.906
MySQL2   0.078   0.072    0.215    0.108      0.275
MongoDB  0.036   0.035    0.036    0.036      0.036

Plot it with line chart

From the above performance data, we can see the DELETE query from MySQL is a O(n) while the TRUNCATE from MySQL and db.TABLE.drop() from MongoDB are both O(1). So when we delete table, we never want to use "DELETE from TABLE" to delete a table from MySQL when the table is considerably large.

##### time to process rich variety

##### Summary

As from the comparative analysis from the above chapters, it is hard to draw a conclusion whether SQL or noSQL is better than the other, because each type of database has its own advantage over the other.

##### Reference

 * http://www.thegeekstuff.com/2014/01/sql-vs-nosql-db/
 * http://www.mongodb.com/nosql-explained
 * http://www.scriptrock.com/articles/mysql-vs-mongodb
 * http://www.tutorialspoint.com/mongodb/index.htm

