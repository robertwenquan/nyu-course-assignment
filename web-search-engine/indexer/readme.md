## Inverted Index Generator

Robert Wen <robert.wen@nyu.edu>  Caicai Chen <caicai.chen@nyu.edu>

#### Introduction

This project is the 2nd programming assignment of the Web Search Engine class for Fall 2015 Semester at Tandon School of Engineering, NYU.

The project is about building an inverted index generator based on web crawled data.

There are two set of web crawled data: NZ dataset and the CommonCrawl dataset. The NZ dataset is with a few million web pages crawled a few years ago for all the New Zealand websites. The CommonCrawl dataset is humongous. For the subset of July 2015 data it's a few dozen TB in crawled data. For this assignment, we select 0.25% of the July 2015 CommonCrawl data for inverted index generation. It is about 80 * 50000 = 4 million pages with about 80 * 150MB = 12GB compressed crawled data.

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

 There are a few core data structures we use for the inverted index building.
 * Word Table
 * URL Table
 * Lexicon
 * Inverted Index

#### Lexicon Building

 * Decompression
  * WARC file is provided with .gz format. We handle both .gz and .wet file for processing. If the file is compressed, it will be decompressed first and read into the memory for processing.
  * We use zlib to process the .gz format.

 * WARC Parsing
  * WARC is a standard protocol to store and archive web contents. We write our own parse to parse the WARC protocol from the uncompressed data.
  * 

 * Lexicon Parsing
  * The payload of each WARC record is the page content.
  * As we use the WET data, the data is stripped out with the HTML tag.
   * Pros of the WET data
    * For simplicity. No need HTML parser
    * For IO efficiency. Less data less IO. It is about 50% size of the
    * For processing efficiency. Lexicon parsing is much easier and faster.
   * Cons of the WET data
    * No context of the lexicons
  * INPUT: raw WET file, either in plaintext format or .gz format
  * OUTPUT: one lexicon file
  * FILE POSTING FORMAT:
   * [WORD_ID][DOC_ID][OFFSET]

 * Lexicon Sorting
  * INPUT: unsorted lexicon file
  * OUTPUT: softed lexicon file
  * Verification


#### Index Building

 * Initial Index Building
  * Since sorted lexicon has the format for each record: [WORD_ID][DOC_ID][OFFSET]
   * Same word occured several times
   * Same doc with same word occured several times
  * After constructint Index:
   * One word occured once in .git file, followed with offset in .mit file, point to docs contain the word 
   * One doc for each word occured once in .mit file, followed with offset in .iidx file, point to places of this word occured in this doc

  * INPUT: sorted lexicon file
  * OUTPUT: inverted index(three files):
     * .git  : [WORD_ID][OFFSET][N_DOCS]
     * .mit  : [DOC_ID][OFFSET][N_PLACES]
     * .iidx : [OFFSET]

 * Index Merging
  * INPUT: List of (.git, .mit) files need to be merged.
  * OUTPUT: one (.git, .mit) file.

  * User can define how many ways to merge, like 8-way, merge at most 8 files each time.
  * User can define how much memory space to use.
  
 * Index bucketing


#### Benchmarks


#### Summary

 * What result have we achieved

 * What we are still lacking

 * What we are going to do next?


#### References


