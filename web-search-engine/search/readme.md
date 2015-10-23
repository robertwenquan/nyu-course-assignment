## README for the search engine

### Overview

This document is about the design and implementation of the search engine, built upon the index created with the second programming assignment.

This project is also a collaborative effort together with Robert Wen and Caicai Chen, from Tandon School of Engineering, with the prior consent of Professor Torsten.

### Architecture

About the architecture. How do we design the search engine. How does the data come out of the index from the word to page content.

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

7. Ranking the pages

We will rank the pages with xxx

After the ranking, we will have a list of 20 pages, with approximate the following information
```
{'docid':322, 'offsets':[3,44,323,2342,34552], 'words':[34,342,33,22,425]}
...
{'docid':482, 'offsets':[3,44,323,2342,34552], 'words':[34,342,33,22,425]}
```

8. Page Retrieval

 8.1 doc meta data retrival

 8.2 word_id to word

9. Result Formatting

Whatever frontend we have, either the Command Line Interface, or the Web GUI, we encode the final output data with JSON for ease of processing.

10. Output

### FAQ

### Benchmarks

 * Search a bag of keywords

 * Search keywords unions

### References

 * BM25
