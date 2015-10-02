## Design of the Web page indexer

### Notes
 * Map Reduce is NOT ALLOWED in this assignment !!!
 * High Speed considering IO Efficiency

### Language??
 * C on EC2
 * Go on EC2
 * Python with MRJob on EMR

### Phase Breakdown
 * Phase1: Generating Lexicons
  * Input: A bunch of NZ or CommonCrawl dataset
  * Output: Parsed lexicons

  * Format: docID, WordID, Pos, Context

  * Steps
   * Uncompress page chunks
   * Parse page and generate lexicons

 * Phase2: Sort each index file (each data file has one index file)
  * Input: Unsorted lexicons
  * Output: Sorted lexicons

  * Sort order: Word ID -> Doc ID -> Position

  * Steps: Merge sort

 * Phase3: Generates stream of postings from set of pages
  * Input: Sorted lexicons
  * Output: Compressed Inverted Files

  * Two output files:
    * Lexicon structure table
      * Format: Word, Offset/Pointer to inner index, Number of docs
    * Inner Index List
      * Format: docID1, Frequence, Pos1, C1, Pos2, C2
                docID2, Frequence, Pos1, C1, Pos2, C2
                ......

* Phase4: Merge Inverted Files(Multi-way)
  * Input: Intermediate Inverted Index
  * Output: Final Inverted Index

  * Think about how to partition lexicon and store in barrels
    * First letter?
    * Alphabetical Range?
    * Hash words into barrals?

=== Modular Breakdown
 * Crawled Page Parser
 * Lexicon Parser
 * N-way merge sort
 * Index Writer

