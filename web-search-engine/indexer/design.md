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

  * Steps
   * Uncompress page chunks
   * Parse page and generate lexicons

 * Phase2: Merge sorting by word IDs
  * Input: multiple files containing unsorted lexicons
  * Output: sorted and merged intermediate format by work ids

  * Steps
   * n-ways merge sorting based on how much memory we have

 * Phase3: Generating RI index on disk
  * Input: a bunch of sorted intermediate format with word ids
  * Output: reversed index files

=== Modular Breakdown
 * Crawled Page Parser
 * Lexicon Parser
 * N-way merge sort
 * Index Writer

