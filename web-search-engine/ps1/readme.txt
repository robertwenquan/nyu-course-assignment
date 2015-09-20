readme.txt file in ascii format with a list of
the files in your submission and what they do, 
and with a short description on how to compile 
and run your program (meaning of input parameters, 
any configuration files etc). Also, point out any 
limitations on parameters (e.g., "query must have
at most 3 words" if that is the case).

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
├── google_crawl.py
├── page_crawl.py
├── utils.py
├── requirements.txt
├── explain.txt
└── readme.txt
