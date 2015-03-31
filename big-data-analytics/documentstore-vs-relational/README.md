## DocumentStore vs Relational Store A comparative Analysis
#### a comparative analysis of MySQL and mongo as dataStores

This paper is a course assignment for the Big Data Analytics class in Spring 2015 semester<br>
Robert Wen (robert.wen@nyu.edu), N12246277, NetID: qw476<br>

##### Introduction

##### Limitations of SQL Engines

* Relational database has scalability concern. While SQL databases have better vertical scalability than noSQL databases, the scaling trend is not linear when the computing resource doulbes more than twice.
* Fixed schema. Everything has to be converted into table schema. Not good for unstructural data. 
* Hierarchical data.
 
##### Limitations of Document Stores 

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

Let's compare the grammar of some common data retrieval tasks from SQL and noSQL

* Add a new record to a data set
* Select a few records from a data set
* Update a value of a record in a data set
* Delete a record from a data set

For SQL: 

* Add: INSERT into TABLENAME (column_name1, column_name2) VALUES(value1, value2);
* Select: SELECT column_name1, column_name2 from TABLENAME;
* Update: UPDATE TABLENAME set column_name1 = value1 WHERE column_name5 == 'Jacky';
* Delete: DELETE from TABLENAME where column_name4 == "NA";

For noSQL:

* Add:
* Select:
* Delete:
* Update:

##### Experimental environment

The following experimental analysis is based on the MySQL and MongoDB instances sponsored by IBM. 

Here is the basic hardware configuration of those two database hosts:

Host   IP Address     CPU                     Memory                  Disk   
-------------------------------------------------------------------------------------------
mysql  174.79.32.150  POWER7 3.3 GHz 80 lcpu  30 GB                   1000 GB
mongo  174.79.32.135  POWER7 3.3 GHz 32 lcpu  30 GB(cross numa-node)  200 GB backed by LVM

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
For MySQL2, we use import command to import all the records in a batch
For MongoDB, we use the following script to perform the records insertion

Database
(INSERT)   100    1000    10000   100000    1000000
---------------------------------------------------
MySQL1
MySQL2
MongoDB

Plot it with line chart

Draw a conclusion based on the above observation:
Which one plays better on small dataset?
Which one plays better on large dataset?
How many records could be inserted in 1s, 1min, 1hr, 1day on MySQL and MongoDB?


##### time to process "n" rows

Process 100 records
Process 1000 records
Process 10000 records
Process 100000 records
Process 1000000 records

Database
(SELECT)   100    1000    10000   100000    1000000
---------------------------------------------------
MySQL     
MongoDB

Plot it with line chart


##### time to update/delete "n" records

Update 100 records
Update 1000 records
Update 10000 records
Update 100000 records
Update 1000000 records

##### time to process rich variety

##### Summary

As from the comparative analysis from the above chapters, it is hard to draw a conclusion whether SQL or noSQL is better than the other, because each type of database has its own advantage over the other.

##### Reference

 * http://www.thegeekstuff.com/2014/01/sql-vs-nosql-db/
 * http://www.mongodb.com/nosql-explained
 * http://www.scriptrock.com/articles/mysql-vs-mongodb

