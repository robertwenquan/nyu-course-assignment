## Notes and Ideas for the indexer: programming assignment 2

* Use mapreduce for C for the indexer
 * https://github.com/google/mr4c

* or MRJob with Python
 * mrjob

* Input

* Output
 * Lexicon structure
  * word/word id
  * inverted index offset
  * length of the RI
 * URL Table
  * docid
  * URL
  * length of the page, etc
 * Inverted Index
  * Positional / Non-positional index
  * docid, frequency, pos1, context, pos2
 * Final index on the disk
  * Just a

* Parsing
 * Parser
  * Parse the pages into tokens, probably with its position
 * Posting
  * docid
  * word id
  * pos
  * context

* Output format
 * ascii or binary
 * a little bit compressed

