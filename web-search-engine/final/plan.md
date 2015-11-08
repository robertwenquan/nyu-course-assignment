## Course Final Project

### Deep Learning Driven Foucused Image Crawler

#### How to do
  * Crawl images from Google/***/*** based on query words

   * Get top 100-1000 result

   * What information can we get from this step?
    * image url
    * any other information?

  * Tag all images with 10k categories classification model
   * Every image has tags and probabilities
   * How to deal with different tags and how to use probabilities??

  * Filter against (IS-A, IS-NOT-A) knowledge graph to increase accuracy
   * Wordnet 
   * Remove less related images

  * Train a model based on KNN
   * k-NN classification? 
   * Every object is being assigned to the class most common among is k nearest neighbours

  * Extend crawl and filter with trainded model

### References

 * WordNet

  * WordNet is a large lexical database of English. Nouns, verbs, adjectives and adverbs are grouped into sets of cognitive synonyms (synsets), each expressing a distinct concept. Synsets are interlinked by means of conceptual-semantic and lexical relations.

  * IS-A: The most frequently encoded relation among synsets is the super-subordinate relation (also called hyperonymy, hyponymy or ISA relation). It links more general synsets like {furniture, piece_of_furniture} to increasingly specific ones like {bed} and {bunkbed}. Thus, WordNet states that the category furniture includes bed, which in turn includes bunkbed; conversely, concepts like bed and bunkbed make up the category furniture. All noun hierarchies ultimately go up the root node {entity}. Hyponymy relation is transitive: if an armchair is a kind of chair, and if a chair is a kind of furniture, then an armchair is a kind of furniture. WordNet distinguishes among Types (common nouns) and Instances (specific persons, countries and geographic entities). Thus, armchair is a type of chair, Barack Obama is an instance of a president. Instances are always leaf (terminal) nodes in their hierarchies.


