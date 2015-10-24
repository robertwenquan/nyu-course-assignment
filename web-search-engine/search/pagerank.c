#include "pagerank.h"

/* 
 * Given a list of words' MIT_T entries, return the union of docs that contain all of the word.
 */

int nextGEQ(MIT_T ** l_docs, int k){
  /*
   * Return the next posting with doc_id >= k in l_docs
   */
  while (*l_docs != NULL) {
    if ((*l_docs)->docid >= k) {
      return (*l_docs)->docid;
    }
    l_docs++;
  }
  return -1;
}

DOCS * get_intersection(MIT_T *** list_word_mit) {
  // Once one MIT_T** reaches NULL, no intersection any more.
  // If read to the last MIT_T ***, return to head.
  if (list_word_mit == NULL) {
    return NULL;
  }
  DOCS * doc_head = NULL; 
  DOCS * doc_tail = NULL;
  DOCS * cur = NULL;

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
      cur = (DOCS *)malloc(sizeof(DOCS));
      if (cur == NULL) {
        return NULL;
      }

      cur->docid = k;
      cur->next = NULL;

      if (doc_head == NULL) {
        doc_head = cur;
        doc_tail = cur;
      } else {
        doc_tail->next = cur;
        doc_tail = cur;
      }
      continuous = 0;
      k++;
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

void cal_BM25(DOC_LIST cur_doc, MIT_T *** list_word_mit, int * count)
{
  /*
   * For each word, IDF(q) = log ( (N-n(q)+0.5) / (n(q)+0.5))
   * Score(D,q) = IDF(q)*( f(q,D)*(k+1) / (f(q,D) + k*(1-b+b*|D|/avgdl)) )
   * Score(D,Q) = sum Score(D,q)
   */
  int N = total_num_docs();
  int D = get_doc_length(cur_doc.docid);
  int avgdl = get_avg_doc_length();

  int k = 2;
  double b = 0.75;

  double idf_q = 0;
  int freq = 0;

  MIT_T * cur = (MIT_T *)malloc(sizeof(MIT_T *));

  while(*list_word_mit != NULL) {
    cur = find_mit_entry(*list_word_mit, cur_doc.docid);
    if (cur == NULL) {
      list_word_mit++;
      continue;
    }
    idf_q = cal_idf_q(N, *list_word_mit);
    freq = cur->n_places;
    *count += freq;
    cur_doc.score += (double) (idf_q * ( freq * (k+1)/ (freq + k*(1-b+b * D/avgdl))));
    list_word_mit++;
  }

  return;
}

MIT_T * find_mit_entry(MIT_T ** list_word_mit, int docid)
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

DOC_LIST * ranking_docs(MIT_T *** list_word_mit)
{
  /* Input : A list of words' MIT_T entries
   * Output: Intersection of docs with BM25 score
   *  1. get_intersection() returns list of intersection docs
   *  2. get_union? use hasing? (TODO)
   *  3. give each docs BM25 score
   *  4. sort docs according to BM25 (TODO)
   *  5. return DOC_LIST
   */
  DOCS * head = get_intersection(list_word_mit);
  DOCS * cur = head;

  int count = 0;
  while (cur != NULL) {
    count ++;
    cur = cur->next;
  }
  cur = head;

  DOC_LIST * docs_list = (DOC_LIST * )calloc(count+1, sizeof(DOC_LIST));

  int i = 0;
  int offsets_size = 0;

  for(i =0; i < count; i++){
    docs_list[i].docid = cur->docid;
    cur = cur->next;
    cal_BM25(docs_list[i], list_word_mit, &offsets_size);
    refill_offsets(docs_list, i, list_word_mit, offsets_size);
  } 
  return docs_list;
}

void refill_offsets(DOC_LIST * doc_list, int place, MIT_T *** list_word_mit, int size)
{
  doc_list[place].offsets = (int *)calloc(size+1, sizeof(int));
  MIT_T * cur_mit = (MIT_T *)calloc(1, sizeof(MIT_T));
  IIDX_T * iidx_list = NULL;
  int count = 0;
  int i = 0;
  while(*list_word_mit != NULL) {
    cur_mit = find_mit_entry(*list_word_mit, doc_list[place].docid);
    if (cur_mit == NULL) {
      list_word_mit++;
      continue;
    }

    iidx_list = query_iindex(cur_mit);
    for(i = 0; i < cur_mit->n_places; i++, count++) {
      doc_list[place].offsets[count] = iidx_list[i].offset;
    }

    list_word_mit++;
  }

  return;
}
double cal_idf_q(int N, MIT_T** l_mit)
{
//IDF(q) = log ( (N-n(q)+0.5) / (n(q)+0.5))  
  int n_q = sizeof(l_mit) / sizeof(MIT_T *)*sizeof(int) - 1;
  double ret = log((N-n_q+0.5)/(n_q+0.5));
  return ret;
}
