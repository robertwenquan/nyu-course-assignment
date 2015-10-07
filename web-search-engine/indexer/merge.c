#include<stdio.h>
#include<stdlib.h>
#include"utils.h"

/**************************************************************************/
/* usage  ./merge maxdegree memsize finlist outfileprefix foutlist        */
/*                                                                        */
/*        maxdegree      : n-way merge                                    */
/*        memsize        : size of available memory in bytes              */
/*        finlist        : name of file containing a list of input files  */
/*        outfileprefex  : directory to record intermediate files         */
/*        foutlist       : name of file containing a list of output files */
/* For example:                                                           */
/*          ./merge 8 4096 finlist fout foutlist                          */
/**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "utils.h"

typedef struct{
    FILE *fgit; 
    FILE *fmit;
    GIT_T* bufgit; 
    MIT_T* bufmit;
    int gitTotal; 
    int gitConsume;
    int mitTotal;
    int mitConsume;} BUF_T;

char * merge_files(char* inputlist, char* path, int numLevel);
//char * testmergeFiles(char* inputlist, char* path, int numLevel);
void write_min(int i, int degree);
int sort_curr(int degree);
int merge_cont(int degree);
void check_ith_mit(int i);
void get_next_word(int i);

BUF_T *ioBufs;
GIT_T *topElem;
int buf_size;
int max_degree;
int mem_size;
int out_offset;

int main(int argc, char* argv[]) {

  max_degree = atoi(argv[1]);
  mem_size = atoi(argv[2]);

  FILE *fin = NULL;
  char filename[1024] = {'\0'};

  int numLevel = 0;
  int inputsize = 0;

  char inputlist[1024] = {'\0'};
  strcpy(inputlist, argv[3]);

  fin = fopen(inputlist, "r");
  if (fin == NULL)
    return -1;

  if (feof(fin)) {
    fclose(fin);
    return -1;
  }

  for (inputsize = 0; !feof(fin) && inputsize<=2; inputsize++) {
    fgets(filename, 1024, fin);
    if (feof(fin))
      break;
  }
  fclose(fin);

  while (inputsize-2) {
    strcpy(inputlist, merge_files(inputlist, argv[4], numLevel));
    numLevel++;
    fin = fopen(inputlist, "r");

    for (inputsize = 0; !feof(fin) && inputsize<=2; inputsize++) {
      fgets(filename, 1024, fin);
      if (feof(fin))
        break;
    }

    fclose(fin);
  }

  printf("%s is the output list\n", inputlist);
  return 0;
}

char* merge_files(char* inputlist, char* path, int numLevel) {
/* Merge files listed in inputlist, every max_degree files produce a new file
   Then return the output list */ 

  FILE *fin = NULL, *fout = NULL;

  int degree = 0;
  int i = 0;
  int numFile = 0;
  char filename[1024] = {'\0'};
  char outfile[1024] = {'\0'};
  char outlist[1024] = {'\0'};
  char outmit[1024] = {'\0'};
  char outgit[1024] = {'\0'};

  unsigned char *buf_space = NULL;
  buf_space = (unsigned char *)malloc(mem_size);
  ioBufs = (BUF_T *)malloc((max_degree + 1) * sizeof(BUF_T));

  sprintf(outlist, "%s%d", path, numLevel);
  fin = fopen(inputlist, "r");
 
  while (!feof(fin)) {
    out_offset = 0;
    //Get source files from the list, assign each file to a BUFFER structure

    for (degree = 0; degree < max_degree; degree++) {
      fscanf(fin, "%s", filename);
      if (feof(fin))
        break;
      ioBufs[degree].fgit = fopen(filename, "r");
      fscanf(fin, "%s", filename);
      if (feof(fin))
        break;
      ioBufs[degree].fmit = fopen(filename, "r");
    }

    if (degree == 0)
      break;

    /* Merge several viles into one file,
       Result of each N files stored in file00, file01, file02...
       Prepared for next level merge */ 
    sprintf(outfile, "%s%d", outlist, numFile);
    sprintf(outgit, "%s%s", outfile, ".git");
    ioBufs[degree].fgit = fopen(outgit, "a");
    sprintf(outmit, "%s%s", outfile, ".mit");
    ioBufs[degree].fmit= fopen(outmit, "a");

    //Give output file more buffer
    buf_size = mem_size / (degree*3 * sizeof(GIT_T));

    for (i = 0; i <= degree; i++) {
      ioBufs[i].bufgit = &(buf_space[ i * sizeof(GIT_T)*buf_size * 2]);
      ioBufs[i].bufmit = &(buf_space[ i * sizeof(GIT_T)*buf_size * 2 + sizeof(GIT_T)* buf_size ]);
      ioBufs[i].gitTotal = 0;
      ioBufs[i].gitConsume = 0;
      ioBufs[i].mitTotal = 0;
      ioBufs[i].mitConsume = 0;
    }
    ioBufs[degree].bufmit= &(buf_space[ degree * sizeof(GIT_T)* buf_size * 2 + sizeof(GIT_T)* buf_size * degree/ 2 ]);
    ioBufs[degree].gitTotal =  buf_size * degree/ 2 ;
    ioBufs[degree].mitTotal = degree * buf_size - buf_size * degree/ 2 ;

    //Merge the current "degree" files
    merge_cont(degree);

    //close files
    for (i = 0; i <= degree; i++) {
      fclose(ioBufs[i].fgit);
      fclose(ioBufs[i].fmit);
    }

    //write the name of output file into outputlist
    fout = fopen(outlist, "a");
    fprintf(fout, "%s\n", outgit);
    fprintf(fout, "%s\n", outmit);
    fclose(fout);

    numFile++;
  }

  fclose(fin); 
  free(ioBufs);
  free(buf_space);

  return outlist;
}

void get_next_word(int i) {
  if (i == -1) {
    return;
  }

  BUF_T *b = &(ioBufs[i]);
  int j,k;
  if ( b->gitTotal == b->gitConsume) {
    for (j = 0; j < buf_size / 2; j++) {
      k = fread(&b->bufgit[j], sizeof(GIT_T), 1, b->fgit);
      if (k == 0)
        break;
    }
    b->gitTotal = j;
    b->gitConsume = 0;  
  }

  if (b->gitTotal == 0) {
    topElem[i].word_id = -1;
    return;
  }

  memcpy(&topElem[i], &(b->bufgit[b->gitConsume]), sizeof(GIT_T));
  b->gitConsume += 1;

  return;
}

int merge_cont(int degree) {
  //Get the minimum of the top element of each buffer
  //Write it into ioBufs[degree], which is the buffer of output file
  //Refill with the next element of this buffer block
  //Until all the buffer block is empty.

  topElem = (GIT_T *)malloc(sizeof(GIT_T) * degree);

  int i;
  for (i = 0; i < degree ; i++) {
    get_next_word(i);
  }
 
  int min = 0;

  while (min >= 0) {
    min = sort_curr(degree);
    write_min(min, degree);
    get_next_word(min);
  } 

  free(topElem);
  return 0;
}

int sort_curr(int degree) {
  //get the minimum word_id and return it's order in buffer

  int minPos = -1;

  int i = 0;
  for (i = 0; i < degree; i++) {
    if (topElem[i].word_id != -1) {
      if (minPos == -1) {
        minPos = i;
      } else if (topElem[i].word_id < topElem[minPos].word_id) {
        minPos = i;
      }
    }
  }

  return minPos;
}

void write_min(int i, int degree) {
  //the ith buffer block is the current minimum word, write it's information to output file.

  BUF_T *b = &ioBufs[i];
  BUF_T *out = &ioBufs[degree];

  //if i==-1, means every buffer is empty, write back everything.
  if (i == -1){
    if (out->gitTotal == out->gitConsume) {
      int j;
      for (j = 0; j < out->gitConsume; j++) {
        fwrite(&(out->bufgit[j]), sizeof(GIT_T), 1, out->fgit);
      }
      out->gitTotal = buf_size * degree/ 2;
      out->gitConsume = 0;
    }
    memcpy(&(out->bufgit[out->gitConsume]), &topElem[degree], sizeof(GIT_T));
    out->gitConsume += 1;
    //fwrite(&(out->bufgit), sizeof(GIT_T)*out->gitConsume, 1, out->fgit);
    int j;
    for (j = 0; j < out->gitConsume; j++) {
      fwrite(&(out->bufgit[j]), sizeof(GIT_T), 1, out->fgit);
    }
    for (j = 0; j < out->mitConsume; j++) {
      fwrite(&(out->bufmit[j]), sizeof(MIT_T), 1, out->fmit);
    }
    return;
  }

  //get the size of docs of that word, write to output buffer one by one.
  int size = topElem[i].n_docs;
  while (size > 0) {
    out_offset += 1;
    //refill content of ith buffer
    if (b->mitTotal == b->mitConsume)
      check_ith_mit(i);
    //If there is no enough space to write a record, flush to disk.
    if (out->mitTotal == out->mitConsume ) {
      int j;
      for (j = 0; j < out->mitConsume; j++) {
        fwrite(&(out->bufmit[j]), sizeof(MIT_T), 1, out->fmit);
      }

      out->mitTotal = degree * buf_size - buf_size * degree/ 2 ;
      out->mitConsume = 0;
    }

    //copy MIT record to output buffer.
    memcpy(&out->bufmit[out->mitConsume], &b->bufmit[b->mitConsume], sizeof(MIT_T));
    b->mitConsume += 1; 
    out->mitConsume += 1;
    size--;
  }

  /*if topElem[i].word_id is different with topElem[degree]
    then write topElem[degree] to output file 
    and update topElem[degree]*/
  if (topElem[i].word_id != topElem[degree].word_id ) {
    if (out->gitTotal == out->gitConsume) {
      int j;
      for (j = 0; j < out->gitConsume; j++) {
        fwrite(&(out->bufgit[j]), sizeof(GIT_T), 1, out->fgit);
      }
      out->gitTotal = buf_size * degree/ 2;
      out->gitConsume = 0;
    }
    if (topElem[i].n_docs != out_offset) {
      memcpy(&(out->bufgit[out->gitConsume]), &topElem[degree], sizeof(GIT_T));
      out->gitConsume += 1;
    }
    memcpy(&topElem[degree], &topElem[i], sizeof(GIT_T));
    topElem[degree].offset = (out_offset - topElem[i].n_docs) * sizeof(GIT_T);
  }else{
    // if they are the same, update topElem[degree].n_docs*/
    topElem[degree].n_docs += topElem[i].n_docs;
  }
  return;
}

void check_ith_mit(int i) {
  //Refill buffer of ioBufs[i]
  BUF_T *b = &ioBufs[i];
  
  int j;
  for (j = 0; j < buf_size ; j++) {
    fread(&b->bufmit[j], sizeof(MIT_T), 1, b->fmit);
  }
  b->mitTotal = j;
  b->mitConsume = 0;
  return;
}

