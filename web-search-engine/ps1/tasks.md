### Break-down tasks for this programming assignment

* Basic Components

 * GSE scraper
  * Owner: Caicai Chen
  * Goal: given a list of keywords, search Google Search Engine and return top 10 URLs
  * Input: a list of keywords
  * Output: top 10 URLs to start crawl to the QUEUE

 * Page scraper
  * Owner: Caicai Chen
  * Goal: fetch and parse the specified URL, generate new relevant URLs to follow up crawling
  * Input: one URL to crawl
  * Output: A list of URLs that are relevant to this topic to the QUEUE

 * Dispatcher
  * Owner: Robert Wen
  * Goal: Fetch task from queue and dispatch the page scraper
  * Input: The queue with URLs to crawl
  * Output: Launch page scraper
  * Termination condition: scraped page # reached N

 * De-duplication Queue
  * Owner: 
  * Goal: Manitain a in-memory cache for URL deduplication

 * Task Queue
  * Owner:
  * Goal: Maintain a FIFO queue for the URLs to be crawled

 * Output and Logging
  * Owner: Robert Wen
  * Goal: Generate proper output files, statistics and log files

* Integration
 * Owner: Robert Wen
 * Goal: Make the individual components glued and work together

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

