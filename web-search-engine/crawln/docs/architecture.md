### Architecture Design

This is the architectural design document of the 'crawlN' web crawler.
crawlN simply means "crawl n web pages". That is what we are going to achieve in this assignment.

#### Overview

Despite we can make it a messy all-in-one crawler in one source file running on local machine, it will not be scalable to make large crawls.
With this consideration, we make two modes to run for this web crawler:

* Local mode: target for testing and small crawls
* Scalable mode: target for large crawls

For the local mode, all of the resources will be used in the local instance, say the laptop

For the scalable mode, it is designed to work on Amazon AWS

#### Terms

* Dispatcher
  * A command line utility to launch, check, and terminate the crawl.
  * This command also is able to query statistics of the historical crawls.

* Worker Thread
  * A thread that is spawned by the worker
  * It crawls and parses only one URL passed by the worker
  * It puts back more URLs back to the Queue for further crawl

* Worker
  * A worker instance that runs on a single compute instance either on a physical or virtualized or cloud based environment.
  * The worker will fetch task(s) from the Queue and launch generic crawl jobs, each in a worker thread
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
  * this block diagram depicts how the basic components are glued together

#### Queue
  * A FIFO queue
  * local mode is based on self implementation
  * scalable mode is based on Amazon AWS SQS (Simple Queue Service)
  * No gurantee the de-queue order is the same as en-queue order
  * Guarantee one fetch per item, no duplicates

#### Storage
  * A directory based persistent storage
  * local mode is based on local filesystem
  * scalable mode is based on Amazon AWS S3 (Simple Storage Service)
  * A unique-crawl-id is used to distinguish multiple crawls
  * s3://<bucket-name>/<crawl-id>/pages
  * s3://<bucket-name>/<crawl-id>/stats.log
  * s3://<bucket-name>/<crawl-id>/crawl.log

