#ifndef _libwarc_h
#define _libwarc_h

#include <assert.h>

typedef struct {
  unsigned int length;
  char warc_ver[8];
  char warc_type[16];
  char content_type[32];
  unsigned int content_length;
  char url[512];
  char *data;
} WARC_HDR_T;

typedef struct {
  unsigned int length;
  char *data;
} WARC_PAYLOAD_T;

typedef struct {
  unsigned int offset;

  WARC_HDR_T * header;
  WARC_PAYLOAD_T * payload;
} WARC_REC_T;


FILE * warc_open(char *filename);
WARC_REC_T * warc_get_next(FILE *warc_fp);
void destroy_warc_rec(WARC_REC_T *warc_rec);
void warc_close(FILE *warc_fp);

#endif

