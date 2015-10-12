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

  * For example:
   * Sorted lexicon:
    word_id  doc_id  offset
       1        1       1
       1        1       3
       1        1       5
       1        2       1

   * .git:
    word_id  offset  n_docs
       1        0       2

   * .mit:
    doc_id   offset  n_places
       1        0       3
       2        3       1

   * .iidx:
     offset
       1
       3
       5
       1

 * Index Merging
  * INPUT: List of (.git, .mit) files need to be merged.
  * OUTPUT: one (.git, .mit) file.

  * Define how many ways to merge, like 8-way, merge at most 8 files each time.
  * Define how much memory space to use.
  * Rewrit .git file and keep one record of same word, add up n_docs, update offset in .mit.
  * Rewrit .mit file, let all docs with same word together.
  * Keep .iidx the same, since these files are large so that it's time consuming to merge together.
  
 * Index bucketing


#### Benchmarks

 Performance matter as it means how much data you can process for this assignment. Due to the time constraint, we only target 4 million docs to index for the assginment submission.

 We have 4 datasets for benchmarking this indexer

 * tiny (3 WET files with 30 docs)
 * small (2 WET files with 100k docs)
 * medium (20 WET files with 1 million docs)
 * large (80 WET files with 4 million docs)

 The way we measure the performance is simple. We use the time command under macos/Linux to measure the run time. The elapsed time is taken for this metrics.

##### Tiny 30
 The tiny dataset is stripped from part of the July 2015 Common Crawl dataset. It is mostly for development and functionality validation purpose. The dataset is not quite useful for performance measurement as it is too small and the whole process finishes so fast in less than one second. Here is a reference number for each phase.

 - lexicon generation  0m0.095s
 - lexicon sorting     0m0.043s
 - index generation    0m0.223s
 - index merge         0m0.006s

 Due to the small amount of time running, there will be big variance in run time when some other processes are running on the same system. Hence it is not a good reference wordload for benchmarking.
 
##### Small 100k
 The small dataset with 100k docs are from 2 unstripped WET files in July 2015 Common Crawl dataset. Each WET file has approximately 50k docs so we have 100k in total. The input dataset is about 470 MB in size.

 Here is the data we collected from our earlier implementation. For quick prototyping, we implemented the first three phases in Python due to the availability of WARC library and easy programming. The whole process takes about 20 minutes.

 - lexicon generation  3m00.881s
 - lexicon sorting     5m24.454s
 - index generation   12m22.024s
 - index merging          4.544s

##### Medium 1m
 The medium dataset with 1 million docs are from 20 unstripped WET files in July 2015 Common Crawl dataset. Each WET file has approximately 50k docs so we have 1 million in total. The input dataset is about 4.7 GB in size.

 Here is the data we collected from our earlier implementation in Python as well. As we can see, the run time is almost linearly growing as the input grows 10 times. The whole process takes a little bit more than 2 hours to complete, which is also fine. But from this estimation it will take more than 20 hours for us to index 10 million documents. And it will take about 3 months to index 1 billion documents.

 - lexicon generation  30m19.675s
 - sorting(python)     57m27.198s
 - index generation    35m50.940s
 - index merging        1m28.378s

 So we re-implemented all phases in C. In the current implenetation, we merged the lexicon generation and sorting in one phase and directly generate the sorted lexicon files. Then we have this performance data.
 - lexicon generation   7m54.576s
 - index generation       40.341s
 - index merging         1m6.245s

##### Large 4m
 The large dataset with 4 million docs are from 80 unstripped WET files in July 2015 Common Crawl dataset. Each WET file has approximately 50k docs so we have 4 million in total. The input dataset is about 19 GB in size.

 With the latest implementation, we have the following performance data

 - lexicon generation  32m10.631s 
 - index generation     3m8.080s 
 - index merging        3m1.799s 

#### Summary
 * What result have we achieved

#### Known Issues
 * What we are still lacking

#### TODO
 * What we are going to do next?

#### References

