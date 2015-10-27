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

  if (verbose) {
    printf("open wet file %s at %d for %d bytes\n", crawl_filename, offset_start, offset_end);
  }

  FILE *fp_crawl = fopen(crawl_filename, "r");
  fseek(fp_crawl, offset_start, SEEK_SET);

  int length = offset_end - offset_start + 1;
  int nread = fread(buf, length, 1, fp_crawl);

  //assert(nread == 1);

  fclose(fp_crawl);
}

/*
 * fetch page content from the doc list
 */
void fetch_doc_list(DOC_LIST * head, int fd)
{

  int pagerank = 0;

  write(fd, "[", 1);

  while(head != NULL) {

    if (head->docid == -1 ){
      break;
    }

    pagerank++;

    printf("\n===== SEARCH RESULT %d =====\n", pagerank);
    if (verbose) {
      printf("- %-8s: %9s\n", "doc url", get_doc_url(head->docid));
      printf("- %-8s: %9d\n", "docid", head->docid);
      printf("- %-8s: %9.2f\n", "score", head->score);
      printf("- %-8s: %9d\n", "offset", *(head->offsets));
      printf("\n");
    }

    if (pagerank != 1) {
      write(fd, ", \n", 3);
    }

    write(fd, "{\"id\":\"", 7);
    char buf[128];
    bzero(buf, 128);
    snprintf(buf, 128, "%d", pagerank);
    write(fd, buf, strlen(buf));
    write(fd, "\", ", 3);

    write(fd, "\"score\":\"", 9);
    char scorebuf[128];
    bzero(scorebuf, 128);
    snprintf(scorebuf, 128, "%.2f", head->score);
    write(fd, scorebuf, strlen(scorebuf));
    write(fd, "\", ", 3);

    write(fd, "\"url\":\"", 7);
    write(fd, get_doc_url(head->docid), strlen(get_doc_url(head->docid)));
    write(fd, "\", ", 3);

    char page_context_buf[256] = {'\0'};
    bzero(page_context_buf, 256);
    get_page_context(head->docid, head->offset_start, head->offset_end, page_context_buf, 256);

    write(fd, "\"context\":\"", 11);
    write(fd, page_context_buf, head->offset_end-head->offset_start+1);
    write(fd, "\"}", 2);

    head++;
  }
}

