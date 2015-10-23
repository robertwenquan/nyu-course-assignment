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

DOC_LIST * get_intersection(MIT_T *** list_word_mit) {
  // Once one MIT_T** reaches NULL, no intersection any more.
  // If read to the last MIT_T ***, return to head.
  if (list_word_mit == NULL) {
    return NULL;
  }

  DOC_LIST * doc_head = NULL;
  DOC_LIST * cur = doc_head;

  int num_words  = sizeof(list_word_mit)/4;
  int continuous = 0;
  int k = 0;
  int ret = 0;
  MIT_T *** p_cur = list_word_mit;

  while (1) {
    if (**p_cur == NULL) {
      break;
    }
    ret = nextGEQ(*p_cur, k);
    if (ret == -1) {
      break;
    } else if (ret == k) {
      continuous++;
    } else {
      k = ret;
      continuous = 1;
    }

    if (continuous == num_words) {
      cur = (DOC_LIST *)malloc(sizeof(DOC_LIST));
      if (cur == NULL) {
        return NULL;
      }

      cur->docid = k;
      cur->score = 0.0;
      cur->url = NULL;
      cur->next = NULL;
      cur = cur->next;
    }

    p_cur++;
    if (*p_cur == NULL) {
      p_cur = list_word_mit;
    }
  }

  return doc_head;
}

int * list_docs(MIT_T *** list_word_mit)
{
  return NULL;
}

void cal_BM25(int docid, MIT_T *** list_word_mit, double * ret)
{
  /*
   * For each word, IDF(q) = log ( (N-n(q)+0.5) / (n(q)+0.5))
   * Score(D,q) = IDF(q)*( f(q,D)*(k+1) / (f(q,D) + k*(1-b+b*|D|/avgdl)) )
   * Score(D,Q) = sum Score(D,q)
   */
  int N = total_num_docs();
  int D = get_doc_length(docid);
  int avgdl = get_avg_doc_length();

  int k = 2;
  double b = 0.75;

  double idf_q = 0;
  int freq = 0;

  MIT_T * cur = (MIT_T *)malloc(sizeof(MIT_T *));

  while(*list_word_mit != NULL) {
    cur = find_doc(*list_word_mit, docid);
    if (cur == NULL) {
      list_word_mit++;
      continue;
    }
    idf_q = cal_idf_q(N, *list_word_mit);
    freq = cur->n_places;
    *ret += (double) (idf_q * ( freq * (k+1)/ (freq + k*(1-b+b * D/avgdl))));
    list_word_mit++;
  }

  return;
}

MIT_T * find_doc(MIT_T ** list_word_mit, int docid)
{
  if (*list_word_mit == NULL) {
    return NULL;
  }
  while ((*list_word_mit)->docid != 0) {
    if ( (*list_word_mit)->docid == docid) {
      return *list_word_mit;
    }
    list_word_mit ++;
  }
  return NULL;
}

char * ranking_docs(int * docs) {
  return NULL;
}

double cal_idf_q(int N, MIT_T** l_mit)
{
//IDF(q) = log ( (N-n(q)+0.5) / (n(q)+0.5))  
  int n_q = sizeof(l_mit) / sizeof(MIT_T *)*sizeof(int) - 1;
  double ret = log((N-n_q+0.5)/(n_q+0.5));
  printf("idf: %f\n", ret);
  return ret;
}
