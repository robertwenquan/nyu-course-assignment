#ifndef _iigen_merge_h
#define _iigen_merge_h

#include <stdio.h>

typedef struct {
  FILE *fgit; 
  FILE *fmit;
  GIT_T* bufgit; 
  MIT_T* bufmit;
  int gitTotal; 
  int gitConsume;
  int mitTotal;
  int mitConsume;
} BUF_T;


void merge_iindex(char **pfilelist);

#endif

