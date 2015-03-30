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
* Delete a record from a data set
* Update a value of a record in a data set

For SQL: 

* Add: INSERT into TABLENAME (column_name1, column_name2, column_name3) VALUES(value1, value2, value3);
* Select: SELECT column_name1, column_name2 from TABLENAME WHERE column_name3 like '%JUNE%';
* Delete: DELETE from TABLENAME where column_name4 == "NA";
* Update: UPDATE TABLENAME set column_name1 = value1 WHERE column_name5 == 'Jacky';

For noSQL:

* Add:
* Select:
* Delete:
* Update:

##### time to add "n" records

##### time to process "n" rows

##### time to update/delete "n" records

##### time to process rich variety

##### Summary

##### Reference

 * http://www.thegeekstuff.com/2014/01/sql-vs-nosql-db/
 * http://www.mongodb.com/nosql-explained
 * http://www.scriptrock.com/articles/mysql-vs-mongodb
