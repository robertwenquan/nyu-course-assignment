/*
 * mostly serve the page fetching from a docid, offset to page text info
 */

#include "page_search.h"
#include "utils.h"


/*
 * the most basic query to a page content
 */

PAGE_CONTEXT_T *get_page_context(int docid, int offset, int length)
{
  char crawl_filename[256] = {'\0'};

  get_wet_filename_from_docid(docid, crawl_filename);

  FILE *fp_crawl = fopen(crawl_filename, "r");

  fseek(fp_crawl, offset, SEEK_SET);

  char *buf = (char *)malloc(length + 1);
  bzero(buf, length + 1);
  int nread = fread(buf, length, 1, fp_crawl);
  assert(nread == 1);

  printf("%s\n", buf);

  fclose(fp_crawl);

  return NULL;
}

/*
 * fetch page content from the doc list
 */
void fetch_doc_list(DOC_LIST * head) {

  int pagerank = 0;

  while(head != NULL) {

    if (head->docid == -1 ){
      break;
    }

    pagerank++;

    printf("===== SEARCH RESULT %d =====\n", pagerank);
    printf("- %-8s: %9d\n", "docid", head->docid);
    printf("- %-8s: %9f\n", "score", head->score);
    printf("- %-8s: %9d\n", "offset", *(head->offsets));
    printf("\n");
    get_page_context(head->docid, *(head->offsets), 60);

    /*
    while(*(head->offsets) != -1) {
      printf(" %-8s: %9d\n", " ", *(head->offsets) );
      (head->offsets)++;
    }
    */

    head++;
  }
}

