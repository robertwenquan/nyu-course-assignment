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
index merge

##### 100k dataset
lexicon generation  3m0.881s     180.881s
sorting(python)     5m24.454s    324.454s
sorting(c)          0m11.042s     11.042s
index generation   12m22.024s    742.024s
index merging

##### 1M dataset
lexicon generation  30m19.675s
sorting(python)     57m27.198s
sorting(c)          
index generation    35m50.940s
index merging        1m28.378s

