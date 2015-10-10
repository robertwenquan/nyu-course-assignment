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

  fseek(fp, 0, 0);

  printf("good...\n");
  return fp;
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
  while (strcmp(buf, "WARC/1.0\r\n") != 0 && feof(warc_fp) == 0) {
    off_start = ftell(warc_fp);
    fgets(buf, 1024, warc_fp);
  }

  if (feof(warc_fp) != 0) {
    return NULL;
  }

  WARC_REC_T * warc_rec = (WARC_REC_T *)malloc(sizeof(WARC_REC_T));
  memset(warc_rec, 0, sizeof(WARC_REC_T));

  warc_rec->offset = off_start;

  return warc_rec;
}

/*
 close the WARC handler
 */
void warc_close(FILE *warc_fp) {
  if (warc_fp) {
    fclose(warc_fp);
  }
}

