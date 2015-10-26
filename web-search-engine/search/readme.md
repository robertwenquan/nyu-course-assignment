## README for the search engine

### Overview

This document is about the design ,implementation and basic usage demo of the search engine, built upon the common crawl index created with the second programming assignment.

This project is also a collaborative effort together with Robert Wen and Caicai Chen, from Tandon School of Engineering, with the prior consent of Professor Torsten.

### Runtime demo

##### How to build
When you untar the tarball, you will come to a directory like this. This is the root of search directory.

```bash
$ tree -d .
.
├── test_data
│   └── tiny30
│       ├── input
│       └── output
└── utils
```
The entire assignment is written in C.

```bash
$ ls -l *.[chp]*
-rw-r--r--  1 robert  staff   2404 Oct 25 12:04 doc_search.c
-rw-r--r--  1 robert  staff    150 Oct 25 11:41 doc_search.h
-rw-r--r--  1 robert  staff   5097 Oct 25 13:34 iindex_search.c
-rw-r--r--  1 robert  staff    275 Oct 25 13:34 iindex_search.h
-rw-r--r--  1 robert  staff    566 Oct 25 11:41 page_search.c
-rw-r--r--  1 robert  staff    253 Oct 25 11:41 page_search.h
-rw-r--r--  1 robert  staff   6987 Oct 25 11:41 pagerank.c
-rw-r--r--  1 robert  staff    671 Oct 24 18:00 pagerank.h
-rw-r--r--  1 robert  staff   4140 Oct 25 12:19 query.c
-rw-r--r--  1 robert  staff    172 Oct 25 11:41 query.h
-rw-r--r--  1 robert  staff     25 Oct 25 11:41 testcases.c
-rw-r--r--  1 robert  staff     40 Oct 25 11:41 testcases.h
-rw-r--r--  1 robert  staff  10691 Oct 25 13:14 utils.c
-rw-r--r--  1 robert  staff   2874 Oct 25 11:41 utils.h
-rw-r--r--  1 robert  staff   4896 Oct 25 13:14 word_search.c
-rw-r--r--  1 robert  staff    143 Oct 24 15:00 word_search.h
```

In the directory, we have prepared the Makefile for you. It is tested on MacOS Yosemite and Ubuntu Linux 14.04. There is no guarantee that will work on other platform but it may work with miminum modification on any unix like systems.

```bash
$ make
...
```

##### How to run
```bash
$ ./search new york city tour
{'query': { 'words': ['new', 'york', 'city', 'tour'], 'npages': 20, 'time': 0.23 }, 
 'result': [
            {'docid':234, 'url':'http://aaaa.aaaa.aaa/aaa/bb/cc/dd/ee', 'qrank':1, 'context':'xxxxxxxxx context'},
            {'docid':234, 'url':'http://aaaa.aaaa.aaa/aaa/bb/cc/dd/ee', 'qrank':1, 'context':'xxxxxxxxx context'}
           ]
}

$ ./search new york city tour | ./search_display_cli.py
Querying ['new', 'york', 'city', 'tour'] from xxxx pages. 0.03s taken.

http://aaaa.aaaa.aaa/aaa/bb/cc/dd/ee
['new', 'york', 'city', 'tour'], qrank: 1
context goes here, with keyword highlighted with yellow color.

http://aaaa.aaaa.aaa/aaa/bb/cc/dd/ee
['new', 'york', 'city', 'tour'], qrank: 1
context goes here, with keyword highlighted with yellow color.

...
END OF SEARCH RESULT
```

Web Demo if we still have time?

### Architecture

 Since all inverted index built in assignment2 are associated with word id instead of real word, so the first step of query is to convert query words into word ids.
 * convert_word_to_ids
   Look into word_table, has the form:
```
    ['new', 12]
    ['york', 15]
```
   Return word id

 After we get word id, we look into the first level of inverted index, which maps word_id to all docs contains this word.
 * query_git
   Use binary search to get GIT entry of word:
```
   { .word_id = 12,
     .offset = 1290,
     .n_docs = 2,
    }
```
    Pass this information to get MIT entries.
 * query_mit
   According to offset given by GIT, find start of MIT entries.
   Given n_docs, read n_docs MIT entry.
```
   { .doc_id = 1,
     .offset = 148,
     .n_places = 2
   }
```

 For each query word, we can get a list of documents, find intersection/union of documents.
 * get_intersection
   Find documents contain all query words, by using nextGEQ.
 * nexGEQ
   Find samllest doc id that is greater or equal to given docid.
 * get_union
   If there is not enough intersection documents, get union of all docs.

 Now we have all documents related to query words, use BM25 to give them score.
 * cal_idf
 * cal_BM25

 According to BM25 score, ranking all document and return first 20 results.
 * sort_doc_list

 Get offset of words in returned 20 documents
 * query_iindex

 Get page content about query words
 * get_page_context

### Data Flow Illustration

1. Acquire the raw query string

Here comes a search of a bag of words, say "tandon nyu 100 million donation"

2. Tokenize and pre-process query string

In the query parser, the words will be split into a list of words, say ["tandon", "nyu", "100", "million", "donation"]. In C Programming, this will be represented like
```
char *list_of_keywords[] = {"tandon", "nyu", "100", "million", "donation", NULL};
```

3. Convert words into word IDs

As we represent words with numeric IDs in all the index files, we need a converstion of words to IDs in order to perform the query.

 * Cons
  * one more translation, seems daunting, but actually it is fast because we use binary search to get the conversion.
 * Pros
  * simplicity in storage. uniform lens of the IDs, rather than the variable length of the words.
  * efficiency in processing. numbers are much more efficient to compare and compute than strings.
  * saving space in storage. Even with an extra table for the word to id mapping, we save space in the index files.

Say we get the following mappings:
{'word':'tandon',   'word_id':12345}
{'word':'nyu',      'word_id':123}
{'word':'100',      'word_id':15}
{'word':'million',  'word_id':1633}
{'word':'donation', 'word_id':6332}

4. Query the GIT(Global Index Table)

This will get doc occurrences of each of the query term(word)
```
{'id':12345, 'ndocs':123, 'where_are_they':offset_in_the_mit}
{'id':123,   'ndocs':23,  'where_are_they':offset_in_the_mit}
{'id':15,    'ndocs':13,  'where_are_they':offset_in_the_mit}
{'id':1633,  'ndocs':435, 'where_are_they':offset_in_the_mit}
{'id':6332,  'ndocs':342, 'where_are_they':offset_in_the_mit}
```

5. Query the MIT(Middle Index Table)

Follow the GIT to MIT, we will have further information about the doc ids containing those terms in additon to how many docs have them. 

We will have some information like below:
```
{'word_id':12345, 'ndocs':123, 'where_are_they':offset_in_the_mit, 'docs':[
 {'docid':342, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 ...[120 docs]...
 {'docid':22, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 {'docid':33342, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
]}
{'word_id':123,   'ndocs':23,  'where_are_they':offset_in_the_mit, 'docs':[
 {'docid':342, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 ...[20 docs]...
 {'docid':45, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 {'docid':984, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
]}
{'word_id':15,    'ndocs':13,  'where_are_they':offset_in_the_mit, 'docs':[
 {'docid':3, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 ...[10 docs]...
 {'docid':452, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 {'docid':766, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
]}
{'word_id':1633,  'ndocs':435, 'where_are_they':offset_in_the_mit, 'docs':[
 {'docid':98, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 ...[433 docs]...
 {'docid':42, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
]}
{'word_id':6332,  'ndocs':342, 'where_are_they':offset_in_the_mit, 'docs':[
 {'docid':43, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
 ...[340 docs]...
 {'docid':30, 'where_to_find_the_term_in_the_doc':'offset_in_the_index'},
]}
```

6. Itersect or union the query results

  Given all query words' MIT entry list, find intersection/union docs. 
  Return a linked list of docids.

  have information like this:
  'docid': 278 -> 'docid':324 -> 'docid':199 -> 'docid':298 -> NULL

7. Score intersection docs

  Give intersection docs BM25 score, and find the MIT entries of the words corresponding to the doc.
  According to MIT entries, list all offsets of queried words in the document.

  With the following form:
  {'docid': 33,   'score': 21.43, 'offset': [1, 2, 4, 10, 25, 28]}
  {'docid': 52,   'score': 24.32, 'offset': [32, 1, 56, 3, 5, 124]}
  {'docid': 125,  'score': 11.46, 'offset': [544, 1235, 32, 5, 23]}
  {'docid': 534,  'score': 34.12, 'offset': [94, 3566, 2, 13, 45, 1345, 12]}
  {'docid': 1363, 'score': 12.56, 'offset': [123, 15, 93, 356, 31]}
  {'docid': 4,    'score': 4.31,  'offset': [12, 490, 455]}
  ...

8. Ranking the pages

We will rank the pages using qsort, in descending order of BM25 score.

After the ranking, we will have a list of 20 pages, with approximate the following information
```
  {'docid': 534,  'score': 34.12, 'offset': [94, 3566, 2, 13, 45, 1345, 12]}
  {'docid': 52,   'score': 24.32, 'offset': [32, 1, 56, 3, 5, 124]}
  {'docid': 33,   'score': 21.43, 'offset': [1, 2, 4, 10, 25, 28]}
  {'docid': 1363, 'score': 12.56, 'offset': [123, 15, 93, 356, 31]}
  {'docid': 125,  'score': 11.46, 'offset': [544, 1235, 32, 5, 23]}
  {'docid': 4,    'score': 4.31,  'offset': [12, 490, 455]}
  ...

```

9. Page Retrieval

 9.1 doc meta data retrival

 Here we need to retrive all the meat data regarding a document. This will answer the following questions:

 - the url of this doc

 But in order to get the above info, we need to figure out this first:
 - which doc index the meta is stored in?
 - from what offset can we find this info?

 9.2 word_id to word

10. Result Formatting

Whatever frontend we have, either the Command Line Interface, or the Web GUI, we encode the final output data with JSON for ease of processing.

11. Output

We use Python wrapper to post-process the raw JSON output and format customized output for CLI or GUI purpose.

### FAQ

1. How fast can you query. 

2. What is the size of the query data size?

3. How long to index?

4. How big the index was in compressed form?

5. How many postings?

6. How long it takes to start up the query processor?

7. How long per query on the queries we gave you?

### Benchmarks

 In order to measure the performance of the search engine, we tried various datasets. For development we use a super tiny dataset with only 30 documents. For quick testing we use a 100k docs dataset for quick verification. We also have another two bigger sets for performance and scalability verification with 1 million and 10 million documents.

 * tiny30
 With only 30 documents for development and quick testing purpose.

 * small100k
 For testing and verification purpose with larger dataset.

 * mid1m

 * large10m
 The final dataset for assignment delivery and demo

### References

 * BM25
   * For each word, IDF(q) = log ( (N-n(q)+0.5) / (n(q)+0.5))
     * N : total number of document
     * n(q) : number of documents contain word "q"

   * Score(D,q) = IDF(q)*( f(q,D)*(k+1) / (f(q,D) + k*(1-b+b*|D|/avgdl)) )
     * f(q,D) : frequency of word "q" in document "D"
     * |D| : length of document "D"
     * avgdl : average length of documents in total dataset
     * In our program, we set k = 2 and b = 0.75

   * Score(D,Q) = sum Score(D,q)
     * Sum of each words' score
