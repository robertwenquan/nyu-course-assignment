/*
 * parser for WARC file format
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "warc.h"

FILE * warc_open(char *filename);
WARC_REC_T * warc_get_next(FILE *warc_fp);
void warc_close(FILE *warc_fp);

/*
 open WARC file
 detect first line whether if it's WARC file format
 by reading the frist 20 bytes
 return the FILE pointer
 */
FILE * warc_open(char *filename) {
  FILE * fp = fopen(filename, "r");
  if (fp == NULL) {
    return NULL;
  }

  char buf[32] = {'\0'};
  int nread = fread(buf, 20, 1, fp);
  if (nread < 1) {
    fclose(fp);
    return NULL;
  }

  if (strstr(buf, "WARC/1.0") != buf) {
    fclose(fp);
    return NULL;
  }

  fseek(fp, 0, SEEK_SET);

  printf("good...\n");
  return fp;
}

static void parse_kv_pair(char *buf, char *key, char *val, int buf_len, int key_len, int val_len) {

  char *pkey = strtok(buf, ":");
  strncpy(key, pkey, key_len);

  char *pval = buf + strlen(key) + 1;
  strncpy(val, pval, val_len);
  val[strlen(val) - 2] = '\0';

  return;
}

static WARC_HDR_T * parse_warc_header (FILE * fp, int offset) {
  fseek(fp, offset, SEEK_SET);

  // parse the header
  // until meet "\r\n"
  char buf[1024] = {'\0'};
  char warc_ver[32] = {'\0'};
  char warc_type[32] = {'\0'};
  char content_type[32] = {'\0'};
  char content_lens[32] = {'\0'};
  char url[512] = {'\0'};

  while (1) {
    fgets(buf, 1024, fp);
    if (strncmp(buf, "\r\n", 2) == 0) {
      break;
    }

    char key[64] = {'\0'};
    char val[256] = {'\0'};
    parse_kv_pair(buf, key, val, 1024, 64, 256);

    if (strncmp(key, "WARC/1.0", 8) == 0) {
      strncpy(warc_ver, "1.0", 32);
    }
    else if (strncmp(key, "WARC-Type", 9) == 0) {
      strncpy(warc_type, val, 32);
    }
    else if (strncmp(key, "Content-Type", 11) == 0) {
      strncpy(content_type, val, 32);
    }
    else if (strncmp(key, "Content-Length", 14) == 0) {
      strncpy(content_lens, val, 32);
    }
    else if (strncmp(key, "WARC-Target-URI", 15) == 0) {
      strncpy(url, val, 32);
    }
  }

  int offset_header_end = ftell(fp);
  int header_length = offset_header_end - offset;
  int content_length = atoi(content_lens);

  fseek(fp, offset, SEEK_SET);
  char *payload = (char *)malloc(header_length);
  int ret = fread(payload, header_length, 1, fp);
  if (ret != 1) {
    free(payload);
    return NULL;
  }
  
  // end of header parsing

  WARC_HDR_T *header = (WARC_HDR_T *)malloc(sizeof(WARC_HDR_T));
  if (header == NULL) {
    free(payload);
    return NULL;
  }

  header->length = header_length;
  strncpy(header->warc_ver, warc_ver, 8);
  strncpy(header->warc_type, warc_type, 16);
  strncpy(header->content_type, content_type, 32);
  header->content_length = content_length;
  strncpy(header->url, url, 512);
  header->data = payload;

  return header;
}

static WARC_PAYLOAD_T * parse_warc_payload (FILE* fp, int length) {
  char *buf = (char *) malloc(length);
  if (buf == NULL) {
    return NULL;
  }

  #ifdef __DEBUG__
  int offset_before_read = ftell(fp);
  #endif

  int nremain = length;
  char *buf_work = buf;
  while (nremain > 0 && feof(fp) == 0) {
    int nbytes = fread(buf, 1, nremain, fp);
    printf("BBBB read %d bytes\n", nbytes);
    nremain -= nbytes;
    buf_work += nbytes;
  }

  #ifdef __DEBUG__
  int offset_after_read = ftell(fp);
  assert(offset_after_read - offset_before_read == length);
  #endif

  WARC_PAYLOAD_T *payload = (WARC_PAYLOAD_T *)malloc(sizeof(WARC_PAYLOAD_T));
  if (payload == NULL) {
    return NULL;
  }

  payload->length = length;
  payload->data = buf;

  return payload;
}

/*
 get the pointer of the next WARC record
 */
WARC_REC_T * warc_get_next(FILE *warc_fp) {
  char buf[1024] = {'\0'};

  if (warc_fp == NULL) {
    return NULL;
  }

  int off_start = 0;
  // find the WARC header
  while (strcmp(buf, "WARC/1.0\r\n") != 0 && feof(warc_fp) == 0) {
    off_start = ftell(warc_fp);
    fgets(buf, 1024, warc_fp);
  }

  if (feof(warc_fp) != 0) {
    return NULL;
  }

  // parse the header
  WARC_HDR_T *header = parse_warc_header(warc_fp, off_start);
  if (header == NULL) {
    return NULL;
  }

  // get the payload
  int content_lens = header->content_length;
  WARC_PAYLOAD_T *payload = parse_warc_payload(warc_fp, content_lens);
  if (payload == NULL) {
    return NULL;
  }

  // make the WARC_REC struct
  WARC_REC_T * warc_rec = (WARC_REC_T *)malloc(sizeof(WARC_REC_T));
  memset(warc_rec, 0, sizeof(WARC_REC_T));

  warc_rec->offset = off_start;
  warc_rec->header = header;
  warc_rec->payload = payload;

  return warc_rec;
}

/*
 * free a WARC_REC_T structure
 * as well as its nested elements
 */
void destroy_warc_rec(WARC_REC_T *warc_rec) {
  if (warc_rec == NULL) {
    return;
  }

  if (warc_rec->header != NULL) {
    WARC_HDR_T *header = warc_rec->header;

    if (header->data != NULL) {
      free(header->data);
    }

    free(warc_rec->header);
  }

  if (warc_rec->payload != NULL) {
    WARC_PAYLOAD_T *payload = warc_rec->payload;

    if (payload->data != NULL) {
      free(payload->data);
    }

    free(warc_rec->payload);
  }
}

/*
 close the WARC handler
 */
void warc_close(FILE *warc_fp) {
  if (warc_fp) {
    fclose(warc_fp);
  }
}

