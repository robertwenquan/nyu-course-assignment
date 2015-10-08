### benchmark data for the indexer

##### Test configuration

* Google Cloud Instance
 * 16 vcpu
 * 16 GB RAM
 * 300 GB SSD

##### 30 dataset
lexicon generation
sorting(python)
sorting(c)
index generation
index merge

##### 100k dataset
lexicon generation  3m0.881s
sorting(python)     5m24.454s
sorting(c)          0m11.042s
index generation   12m22.024s
index merging

