### Architecture Design

This is the architectural design document of the 'crawlN' web crawler.
crawlN simply means "crawl n web pages". That is what we are going to achieve in this assignment.

#### Overview

Despite we can make it a messy all-in-one simple crawler, it will not be scalable to make large crawls.
So we make two modes to run for this web crawler:

* Local mode
 * Target for testing and small crawls
* Scalable mode
 * Target for large crawls

#### Terms

* Dispatcher
  * A command line utility to launch, check, and terminate the crawl.
  * This command also is able to query statistics of the historical crawls.

* Worker
  * A worker instance that runs on a single compute instance either on a physical or virtualized or cloud based environment.
  * The worker will fetch task from the Queue and launch generic crawl job in a thread
  * The worker will run on Amazon AWS EC2

* Worker Group
  * A group of workers, each of which runs independently on a physical, virtualized, or cloud based host.
  * A group could be with one or more instances.
  * The number of instances could be specified at launch, or adjusted during crawl, on the dispatcher.
  * Amazon AWS EC2 AutoScalingGroup will be used for this

* Queue
  * A Message Queue service that runs independently
  * Connected with dispatcher and crawlers with network interface
  * Use unique crawl-id to distinguish multiple crawls
  * Amazon AWS SQS will be used for this

* Cache
  * A In-memory database serving as a cache for URL deduplication
  * Use unique crawl-id to distinguish multiple crawls
  * Amazon AWS ElasticCache will be used for this

* Storage
  * A persistent storage service for storing crawled page, logs, and statistics
  * Amazon AWS S3 will be used for this

#### Block Design

#### Queue

#### Storage

