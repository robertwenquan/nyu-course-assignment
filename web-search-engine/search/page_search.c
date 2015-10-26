/*
 * mostly serve the page fetching from a docid, offset to page text info
 */

#include "page_search.h"
#include "utils.h"


/*
 * the most basic query to a page content
 */

static void get_page_context(int docid, int offset_start, int offset_end, char *buf, int buflen)
{
  char crawl_filename[256] = {'\0'};

  get_wet_filename_from_docid(docid, crawl_filename);

  FILE *fp_crawl = fopen(crawl_filename, "r");
  fseek(fp_crawl, offset_start, SEEK_SET);

  int length = offset_end - offset_start + 1;
  int nread = fread(buf, length, 1, fp_crawl);
  assert(nread == 1);

  fclose(fp_crawl);
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
    if (verbose) {
      printf("- %-8s: %9d\n", "docid", head->docid);
      printf("- %-8s: %9f\n", "score", head->score);
      printf("- %-8s: %9d\n", "offset", *(head->offsets));
      printf("\n");
    }

    printf("%s\n", get_doc_url(head->docid));
    char page_context_buf[256] = {'\0'};
    bzero(page_context_buf, 256);
    get_page_context(head->docid, head->offset_start, head->offset_end, page_context_buf, 256);

    printf("%s\n", page_context_buf);

    head++;
  }
}

