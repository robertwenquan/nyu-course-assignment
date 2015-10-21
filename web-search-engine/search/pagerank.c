#include "pagerank.h"

/* 
 * Given a list of words' MIT_T entries, return the union of docs that contain all of the word.
 */

int nextGEQ(MIT_T ** l_docs, int k){
  /*
   * Return the next posting with doc_id >= k in l_docs
   */
  while (*l_docs != NULL) {
    if ((*l_docs)->docid > k) {
      return (*l_docs)->docid;
    }
    l_docs++;
  }
  return -1;
}

int * get_intersection(MIT_T *** list_word_mit) {
  
  return NULL;
}

float cal_BM25 (int docid) {
  return 0;
}

char * ranking_docs(int * docs) {
  return NULL;
}
