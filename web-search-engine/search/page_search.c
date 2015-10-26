/*
 * mostly serve the page fetching from a docid, offset to page text info
 */

#include "page_search.h"
#include "utils.h"


/*
 * the most basic query to a page content
 */

PAGE_CONTEXT_T *get_page_context(int docid, int offset)
{
  char crawl_filename[256] = {'\0'};

  get_wet_filename_from_docid(docid, crawl_filename);

  FILE *fp_crawl = fopen(crawl_filename, "r");

  fseek(fp_crawl, offset, SEEK_SET);

  char buf[33] = {'\0'};
  bzero(buf, 33);
  fread(buf, 32, 1, fp_crawl);

  fclose(fp_crawl);

  return NULL;
}

