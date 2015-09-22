### Break-down tasks for this programming assignment

* Basic Components

 * GSE scraper
  * Owner: Caicai Chen
  * Goal: given a list of keywords, search Google Search Engine and return top 10 URLs
  * Input: a list of keywords
  * Output: top 10 URLs to start crawl to the QUEUE
  * Status: Finished

 * Page scraper
  * Owner: Caicai Chen
  * Goal: fetch and parse the specified URL, generate new relevant URLs to follow up crawling
  * Input: one URL to crawl
  * Output: A list of URLs that are relevant to this topic to the QUEUE
  * Status: Finished

 * Page Scorer
  * Owner: Caicai Chen
  * Goal: score the page based on comprehensive strategies
  * Input: page url, page title, page content of the crawled page
  * Output: page score
  * Status: In Progress

 * Dispatcher
  * Owner: Robert Wen
  * Goal: Fetch task from queue and dispatch the page scraper
  * Input: The queue with URLs to crawl
  * Output: Launch page scraper
  * Termination condition: scraped page # reached N
  * Status: Finished

 * De-duplication Queue
  * Owner: Robert Wen
  * Goal: Manitain a in-memory cache for URL deduplication

 * Task Queue
  * Owner: Robert Wen
  * Goal: Maintain a FIFO queue for the URLs to be crawled

 * Output and Logging
  * Owner: Robert Wen
  * Goal: Generate proper output files, statistics and log files

* Integration
 * Owner: Robert Wen
 * Goal: Make the individual components glued and work together
 * Features: argument parsing, configuration file, multi-threading, etc.
 * Status: In Progress

* Testing
 * Owner: Caicai Chen
 * Goal: Proper test cases to have 90%+ code coverage of the project

* Documentation
 * Owner: Caicai Chen, Robert Wen (for individual component)
 * Goal: Clear documentation about the design and implementation

* Link examples
 * <a href=link_url>text</a>
 * <a href=http://sdfs.sdfs.fsdf./sfsdfdf>text</a>
 * <a href=sfsdfdf/sdfsd/sdfsd.html>text</a>

