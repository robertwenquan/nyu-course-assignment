## Developer Manual for iigen

#### Development Environment
* We use google cloud compute instance for development
 * IP: 104.196.1.253
  * 16 vCPU
  * 16 GB RAM
  * 400 GB SSD
  * 10 GB buffered write in 524 MB/s
  * 10 GB unbuffered read in 485 MB/s

 * IP: 23.236.58.54
  * 32 vCPU
  * 200 GB RAM
  * 1TB SSD

#### Dataset
* dataset1 (30 docs in 3 wet files)
 * each wet file with 10 docs
 * under test_data

* dataset1 (100k docs in 2 wet files)
 * each wet file with approx 50k docs
 * under google instance /data/wse/100k

#### Libraries we use
* libyaml
 * brew install libyaml on mac
 * libyaml already installed on google instance
 * include <yaml.h>

