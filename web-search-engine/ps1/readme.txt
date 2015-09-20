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
    ├── requirements.txt            # required modules
    ├── explain.txt                 # description of how the program works
    └── readme.txt                  # diretory structure and instruction

2. How to run

  i) Prepare to run:
      Install Python 2.7
      Install nosetest

  ii) Run the program:
      $ python crawln.py [-n [NUM]] [keyword [keyword ...]]

      Examples:
        Default with search 'nyu poly' with 10 pages
        $ python crawln.py

        The following launch will search 'nyu poly computer science' and crawl 1000 pages
        $ python crawln.py -n 1000 'nyu poly computer science'

3. How to Test

  We use unittest and nosetest to test this code base
  Run in top directory:
    $ nosetest
