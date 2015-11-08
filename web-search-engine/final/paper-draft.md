# Self-learning target image crawler

NYU Tandon School of Engineering, Department of Computer Science
Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>

### Abstract

In the web search engine, it is built upon inverted index with text. (Write something about the text search engine and find some reference about it)

Image search (image.google.com) is also built upon inverted index with image meta data. But the image meta data is not readility available. There are various known approaches to get meta data for the images(???? need some research). But all of them need human intervention classification. For payed labeled data the accuracy is usually good enough. But for community and social media generated data, which are the major contribution of the data in the world. (??? data how many images generated per year?) The noise is very high and searching. Finding larget amount of pictures with a topic is actually a big challenge. If you search through google image, you will see a hundred of pictures with pretty good relevance and quality. But if you keep scrolling down a little bit you will even see a bunch of outliers. If we go out to social media website like Flickr, Twitter, Tumblr, etc. 

### 1. Introduction

### 2. System Components

#### 2.1 The seed crawl

Starting with a list of keywords, a seed crawl will start with a list of "good quality" picture source website.
google image search is chosen by default.
This crawl is supposed to finish very fast with a limited scope crawl, say 100 picture samples.

We also tried to extend the seed crawl outside of google image search to add more variety to the samples. In addition to the variety, much more noise are also added. So the accuracy of the seed crawl may drop but this may improve the generalization of the model trained from the samples after we filter with tag based or clustering based filtering.

#### 2.2 Filter the seeds

##### 2.2.1 No filter

For this approach, we do nothing but leave all the samples from the seed crawl. Those samples will be used for the model training.

##### 2.2.2 Filter by tag

With the tagging serivce by Clarifai API, a bunch of tags will be predicted for each image sample. Instead of doing a hard tag matching, we use the wordnet data to map the search term into knowledge graph and logically compare the predicted concepts against the search concepts. If there is any obvious logical contradition, we will treat the crawled sample as negative and evict it from the sample pool. 

The evict ratio and survival rate will be measured for this filtering strategy.

##### 2.2.3 Filter by clustering

In addition to the predicted labels, feature embedding is also returned from Clarifai API. This is a high dimensional array for each image. With the KNN clustering, we could probably get a few clusters of images. We will leave the cluster with the top frequencies and throw all the others away.

The evict ratio and survival rate will be measured for this filtering strategy.

##### 2.2.4 Extend the seed crawl

If it happens to have too few samples after the filter.

#### 2.3 Training on the seed samples

After the filtering from 2.2, we will have a subset of the seed crawl.

#### 2.4 Iterate the crawl and train

### 4. Results and Performance

#### .1 Test Environment and Method

Although we only target the accuracy rather than throughput or latency which usually depends on computing power, we also run all the experiments on Amazon AWS EC2 instances. One of the reasons is because the good network bandwidth on the cloud. The other major reason is the consideration of research continuity because frequent crawls are easily to be caught and banded from various sources. By simply restarting the EC2 instance with another IP address the research would not be blocked. 

#### .2 Test data

For the test data, we leveraged the open data contributed by Microsoft COCO dataset. How to use it?

### Conclusion

### Acknowledgements

### References

 * xxxx
 * xxxx
 * xxxx
 * mscoco dataset reference

