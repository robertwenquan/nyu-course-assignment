## FAQ (Frequent Asked Questions)

* What Python version is this crawler based on?
 * Python 2.7

* What libraries are used for this crawler?
 * requests for HTTP request
 * beautifulsoup4 for HTML parsing
 * unittest and nose for unit testing

* Is the crawler multi-threaded?
 * YES. We are using threading module

* What queueing mechanism are used?
 * We use priority queue to manage the page crawl
 * We use a simple FIFO queue for the crawl logging

* What exceptions does the crawl handle?
 * Overall network connection failure
 * Network connection during crawl
 * Unresolvable URL

