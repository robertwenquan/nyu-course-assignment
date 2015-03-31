DROP TABLE IF EXISTS flickr_pics;
CREATE TABLE flickr_pics (timestamp long, imgurl varchar(256), blogurl varchar(256), labels varchar(512));
load data infile "/home/9223/qw476/sql_vs_nosql/data/flickr-100000.tab" into table flickr_pics columns terminated by '\t' lines terminated by '\n';
