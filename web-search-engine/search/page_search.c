/*
 * mostly serve the page fetching from a docid, offset to page text info
 */

#include "page_search.h"

int get_abs_offset(int docid, int offset)
{
  return offset;
}

FILE *get_crawl_fp_from_docid(int docid)
{
  return NULL;
}

/*
 * the most basic query to a page content
 */

PAGE_CONTEXT_T *get_page_context(int docid, int offset)
{
  char crawl_filename[256] = {'\0'};
  bzero(crawl_filename, 256);

  FILE *fp_crawl = get_crawl_fp_from_docid(docid);

  URL_IDX_T *p_doc_meta = get_doc_meta(docid);
  
  fseek(fp_crawl, offset, SEEK_SET);

  return NULL;
}

