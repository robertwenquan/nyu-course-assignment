### Break-down tasks for this programming assignment

* Basic Components
 * GSE scraper
  * Goal: given a list of keywords, search Google Search Engine and return top 10 URLs
  * Input: a list of keywords
  * Output: top 10 URLs to start crawl to the QUEUE
 * Page scraper
  * Goal: fetch and parse the specified URL, generate new relevant URLs to follow up crawling
  * Input: one URL to crawl
  * Output: A list of URLs that are relevant to this topic to the QUEUE
 * Dispatcher
  * Goal: Maintain a queue and dispatch the page scraper
  * Input: The queue with URLs to crawl
  * Output: Launch page scraper
  * Termination condition: scraped page # reached N

* Integration
 * Goal: Make the basic components work together

