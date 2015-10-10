#ifndef _libwarc_h
#define _libwarc_h

typedef struct {
  unsigned int length;
  unsigned char warc_ver[8];
  unsigned char warc_type[16];
  unsigned char content_type[32];
  unsigned char *url;
  unsigned char *data;
} WARC_HDR_T;

typedef struct {
  unsigned int length;
  char *data;
} WARC_PAYLOAD_T;

typedef struct {
  unsigned int offset;

  WARC_HDR_T header;
  WARC_PAYLOAD_T payload;
} WARC_REC_T;


FILE * warc_open(char *filename);
WARC_REC_T * warc_get_next(FILE *warc_fp);

#endif

