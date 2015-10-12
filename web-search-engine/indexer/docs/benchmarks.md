### benchmark data for the indexer

##### Test configuration

* Google Cloud Instance
 * 16 vcpu
 * 16 GB RAM
 * 300 GB SSD

##### 30 dataset
lexicon generation  0m0.095s
sorting(python)     0m0.043s
sorting(c)          0m0.003s
index generation    0m0.223s
index merge         0m0.006s

##### 100k dataset (mixed with Python and C)
lexicon generation  3m0.881s     180.881s
sorting(python)     5m24.454s    324.454s
index generation   12m22.024s    742.024s
index merging          4.544s      4.544s

##### 1M dataset
lexicon generation  30m19.675s
sorting(python)     57m27.198s
index generation    35m50.940s
index merging        1m28.378s

##### 100k dataset (all in C)
lexicon generation    50.134s
index generation       3.522s
index merging          4.544s

##### 1M dataset (all in C)
lexicon generation   7m54.576s
index generation       40.341s
index merging         1m6.245s

##### 4M dataset (all in C)
lexicon generation  32m10.631s 
index generation     3m8.080s 
index merging        3m1.799s 

##### 10M dataset (all in C)

