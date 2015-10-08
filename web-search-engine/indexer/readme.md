## Inverted Index Generator

#### Introduction

This project is the 2nd programming assignment of the Web Search Engine class for Fall 2015 Semester at Polytechnic School of Engineering, NYU.

The project is about building an inverted index generator based on web crawled data.

There are two set of web crawled data: NZ dataset and the CommonCrawl dataset. The NZ dataset is with a few million web pages crawled a few years ago for all the New Zealand websites. The CommonCrawl dataset is humongous. For the subset of July 2015 data it's a few dozen TB in crawled data. For this assignment, we select 0.1% of the July 2015 CommonCrawl data for inverted index generation. It is about 35 * 50000 = 1.7 million pages with about 35 * 150MB = 5.2GB compressed crawled data.

This document describes the design of the inverted index builder.

#### Architecture

 We implemente the indexer with multiple phases.
 * warc parsing
 * lexicon generation
 * lexicon sorting
 * index generation
 * index merging
 * index bucketing


#### Core Data Structure


#### Lexicon Building

 * Decompression

 * WARC Parsing

 * Lexicon Parsing

 * Lexicon Sorting


#### Index Building

 * Initial Index Building

 * Index Merging

 * Index bucketing


#### Benchmarks


#### Summary

 * What result have we achieved

 * What we are still lacking

 * What we are going to do next?


#### References

