readme.txt file in ascii format with a list of
the files in your submission and what they do, 
and with a short description on how to compile 
and run your program (meaning of input parameters, 
any configuration files etc). Also, point out any 
limitations on parameters (e.g., "query must have
at most 3 words" if that is the case).

1. Directory tree
    .
    ├── docs                        # various documents in this folder
    │   ├── architecture.md
    │   ├── benchmarks.md
    │   ├── readme.md
    │   ├── spec.md
    │   └── tasks.md
    ├── notebook                    # ipython notebook for code snippets and experiments
    │   ├── google.xml
    │   └── parse_google_page.ipynb
    ├── tests                       # python unittest test cases
    │   ├── test_dedupe_cache.py
    │   ├── test_google_crawl.py
    │   ├── test_page_crawl.py
    │   └── test_task_queue.py
    ├── crawln.yml                  # configuration file in yaml format
    ├── settings.py                 # crawler setting classes
    ├── crawln.py                   # crawler launch program
    ├── crawln_dispatcher.py        # crawler dispatcher class
    ├── google_crawl.py             # Google web search class
    ├── bing_crawl.py               # Bing web search class
    ├── page_crawl.py               # Generic web page crawler and parser
    ├── validation_check.py         # Simplify url functions
    ├── utils.py                    # TaskQueue, DeDupCache, Logger classes
    ├── worker.py                   # Worker thread class
    ├── requirements.txt            # required modules
    ├── explain.txt                 # description of how the program works
    └── readme.txt                  # diretory structure and instruction

2. How to run

  i) Prepare to run:
      Install Python 2.7
      Install pip
      $ pip install -r requirements.txt

  ii) Configuration
      crawln.yml is the configuration file of the crawler

  iii) Run the program:
      $ python crawln.py [-n [NUM]] [keyword [keyword ...]]

      Examples:
        Default run with no arguments is a crawl for 'nyu poly' with 10 pages
        $ python crawln.py

        The following launch will search 'nyu poly computer science' and crawl 1000 pages
        $ python crawln.py -n 1000 'nyu poly computer science'

   iv) Check the results
       After a normal crawl, the following files will be generated:
        /tmp/crawl.log      - crawl log for the pages
        /tmp/crawl.stats    - crawl statistics
        /tmp/crawln/*       - crawl page contents

       /tmp/crawl.log
        $ jq '.' /tmp/crawl.log | head -n12
        {
          "code": 200,
          "linkhash": "883be962711be18e485ce2dc141af0ea",
          "depth": 1,
          "score": 8,
          "start": "Sun Sep 20 18:55:04 2015",
          "url": "http://engineering.nyu.edu/academics/graduate-school",
          "time": 5.362926006317139,
          "ref": "",
          "store": "88/3b/e962711be18e485ce2dc141af0ea",
          "size": 18939
        }

       /tmp/crawl.stats
        $ cat /tmp/crawl.stats
        Crawl   start: Sun Sep 20 18:55:01 2015
        Crawl    stop: Sun Sep 20 18:55:13 2015
        Crawl    time: 11.6 secs
        Crawled pages:              10 (0.9 pages / sec)
        Crawled bytes:         1225714 (105873 bytes / sec)

       /tmp/crawln/*
        $ find /tmp/crawln -type f
        /tmp/crawln/28/ce/d15a8d80202925603bca1443fc33
        /tmp/crawln/49/db/62a5f526b128aff92e11fcfc415d
        /tmp/crawln/85/83/0d6dd40fb1bd509f9ecfcd922b0d
        /tmp/crawln/88/3b/e962711be18e485ce2dc141af0ea
        /tmp/crawln/8f/38/009061c369d90d918172635f091c
        /tmp/crawln/aa/b1/2fce27ba4cff0a711fcb8819024b
        /tmp/crawln/b9/5b/091e30029d35a54876d8f8387767
        /tmp/crawln/d7/b1/964f0838bda8ff0283629ee0843d
        /tmp/crawln/d9/9e/a4604151f1af09f91977d3732f65
        /tmp/crawln/df/a8/b72ca1b8ffa91e32680f756e918a

3. How to Test

  We use unittest and nosetest to test the code base
  Run in top directory of this project:

    $ nosetests -v
    test bing top 10 search crawler ... ok
    test bing top 10 search crawler ... ok
    test de-dupe with 100k URLs ... ok
    test de-dupe simple case with 3 URLs ... ok
    test DeDupeCache() class initialization ... ok
    test google top 10 search crawler ... ok
    test google top 10 search crawler ... ok
    test_blacklist (test_page_crawl.TestPageCrawl) ... ok
    test normalize url function ... ok
    test generic page crawler initialization ... ok
    test_simplify_url (test_page_crawl.TestPageCrawl) ... ok
    test_bulk_enqueue_dequeue (test_task_queue.TestTaskPriorityQueue) ... ok
    test_init (test_task_queue.TestTaskPriorityQueue) ... ok
    test_simple_enqueue_dequeue (test_task_queue.TestTaskPriorityQueue) ... ok

    ----------------------------------------------------------------------
    Ran 14 tests in 13.129s

    OK

  
