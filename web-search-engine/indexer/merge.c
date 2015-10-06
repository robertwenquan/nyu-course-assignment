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
  FILE *f; 
  FILE *fcont;
  char* buf; 
  char* bufcont;
  int tableTotal; 
  int tableConsume;
  int contTotal;
  int contConsume;
} BUF_T;

void MergeCont();
char * mergeFiles(char* inputlist, char* path, int numLevel);
char * testmergeFiles(char* inputlist, char* path, int numLevel);
void writeMin(int i, int degree);
int sortCurr(int degree);
void checkIContent(int i);

BUF_T *ioBufs;
GIT_T *topElem;
int bufSize;
int maxDegree;
int memSize;

int main(int argc, char* argv[]) {

  maxDegree = atoi(argv[1]);
  memSize = atoi(argv[2]);

  FILE *fin = NULL;
  char filename[1024] = {'\0'};

  int numFiles = 0;
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

  for (inputsize = 0; !feof(fin) && inputsize<=1; inputsize++) {
    fgets(filename, 1024, fin);
    if (feof(fin))
      break;
  }
  fclose(fin);

  while (inputsize - 1) {
    strcpy(inputlist, mergeFiles(inputlist, argv[4], numLevel));
    numLevel++;
    fin = fopen(inputlist, "r");

    for (inputsize = 0; !feof(fin) && inputsize<=1; inputsize++) {
      fgets(filename, 1024, fin);
      if (feof(fin))
        break;
    }

    fclose(fin);
  }

  printf("%s is the output list\n", inputlist);
  return 0;
}

char* mergeFiles(char* inputlist, char* path, int numLevel) {
/* Merge files listed in inputlist, every maxDegree files produce a new file
   Then return the output list */ 

  FILE *fin, *fout;

  int degree;
  int i;
  int numFile = 0;
  int bufSize;

  char filename[1024];
  char outfile[1024];
  char outlist[1024];
  char outcont[1024];

  char *bufSpace;
  bufSpace = (unsigned char *)malloc(memSize);
  ioBufs = (BUF_T *)malloc((maxDegree + 1) * sizeof(BUF_T));

  sprintf(outlist, "%s%d", path, numLevel);
  fin = fopen(inputlist, "r");
 
  while(!feof(fin)) {
    //Get source files from the list, assign each file to a BUFFER structure

    for(degree = 0; degree < maxDegree; degree++) {
      fscanf(fin, "%s", filename);
      if (feof(fin))
        break;

      ioBufs[degree].f = fopen(filename, "r");

      //TODO: GET the name of MIT_T table
      ioBufs[degree].fcont = fopen(filename, "r");
    }

    if(degree == 0)
      break;

    /* Merge several viles into one file,
       Result of each N files stored in file00, file01, file02...
       Prepared for next level merge */ 
    sprintf(outfile, "%s%d", outlist, numFile);
    ioBufs[degree].f = fopen(outfile, "w");
    sprintf(outcont, "%s%s", outfile, ".cont");
    ioBufs[degree].fcont = fopen(outcont, "w");

    //Give output file more buffer
    bufSize = memSize / (degree*3);

    for(i = 0; i <= degree; i++) {
      ioBufs[i].buf = &(bufSpace[ i * bufSize * 2]);
      ioBufs[i].bufcont = &(bufSpace[ i * bufSize * 2 + bufSize / 2 ]);
      ioBufs[i].tableTotal = 0;
      ioBufs[i].tableConsume = 0;
      ioBufs[i].contTotal = 0;
      ioBufs[i].contConsume = 0;
    }

    ioBufs[degree].bufcont = &(bufSpace[ degree * bufSize * 2 + bufSize * degree/ 4 ]);
    ioBufs[degree].tableTotal = bufSize * degree/ 4 ;
    ioBufs[degree].contTotal = degree * bufSize - bufSize * degree/ 4 ;

    //Merge the current "degree" files
    mergeCont(degree);

    //close files
    for(i = 0; i <= degree; i++) {
      fclose(ioBufs[i].f);
      fclose(ioBufs[i].fcont);
    }

    //write the name of output file into outputlist
    fout = fopen(outlist, "a");
    fprintf(fout, "%s\n", outfile);
    fclose(fout);

    numFile++;
  }

  fclose(fin); 
  free(ioBufs);
  free(bufSpace);

  return outlist;
}

void getNextWord(int i) {

  if(i == -1) {
    return;
  }

  BUF_T *b = &(ioBufs[i]);

  if ( b->tableTotal - b->tableConsume < sizeof(GIT_T)) {
    b->tableTotal = fread(&(b->buf), (bufSize/sizeof(GIT_T)*sizeof(GIT_T)), 1, b->f);
    b->tableConsume = 0;  
  }

  if (b->tableTotal == 0) {
    topElem[i].word_id = -1;
    return;
  }

  memcpy(&topElem[i], &(b->buf[b->tableConsume]), sizeof(GIT_T));
  b->tableConsume += sizeof(GIT_T);

  return;
}

int mergeCont(int degree) {
  //Get the minimum of the top element of each buffer
  //Write it into ioBufs[degree], which is the buffer of output file
  //Refill with the next element of this buffer block
  //Until all the buffer block is empty.

  GIT_T *lastRecord;
  topElem = (GIT_T *)malloc(sizeof(GIT_T) * degree);

  int i = 0;
  for (i = 0; i < degree - 1; i++) {
    getNextWord(i);
  }
 
  int min = 0;
  while(min >= 0) {
    min = sortCurr(degree-1);
    writeMin(min, degree);
    getNextWord(min);
  } 

  return 0;
}

int sortCurr(int degree) {
  //get the minimum word_id and return it's order in buffer

  int minPos = -1;

  int i = 0;
  for (i = 0; i < degree; i++) {
    if (topElem[i].word_id != -1) {
      if (minPos == -1) {
        minPos = i;
      } else if(topElem[i].word_id < topElem[minPos].word_id) {
        minPos = i;
      }
    }
  }

  return minPos;
}

void writeMin(int i, int degree) {
  //the ith buffer block is the current minimum word, write it's information to output file.

  BUF_T *b = &ioBufs[i];
  BUF_T *out = &ioBufs[degree];

  //if i==-1, means every buffer is empty, write back everything.
  if (i == -1) {
    fwrite(&(out->buf), out->tableConsume, 1, out->f);
    fwrite(&(out->bufcont), out->contConsume, 1, out->fcont);
  }

  //get the size of docs of that word, write to output buffer one by one.
  int size = topElem[i].n_docs;
  while (size > 0) {
    if (out->contTotal - out->contConsume < sizeof(MIT_T)) {
      fwrite(&(out->bufcont), out->contConsume, 1, out->fcont);
      out->contTotal = degree*bufSize - bufSize*degree/4 ;
      out->contConsume = 0;
      break;
    }

    //refill content of ith buffer if there's not enough left
    checkIContent(i);

    memcpy((void *)(out->bufcont[out->contConsume]), (void *)(b->bufcont[b->contConsume]), sizeof(MIT_T));
    b->contConsume += sizeof(MIT_T);
    out->contConsume += sizeof(MIT_T);
    size--;
  }

  //if topElem[i].word_id is different with topElem[degree], then write topElem[degree] to output file and update topElem[degree], if they are the same, update topElem[degree].n_docs
  if (topElem[i].word_id != topElem[degree].word_id) {
    if (out->tableTotal - out-> tableConsume < sizeof(GIT_T)) {
      fwrite(&(out->buf), out->tableConsume, 1, out->f);
      out->tableTotal = bufSize * degree/ 4;
      out->tableConsume = 0;
    }

    memcpy(&(out->buf), &topElem[degree], sizeof(GIT_T));
    out->tableConsume += sizeof(GIT_T);
    memcpy(&topElem[degree], &topElem[i], sizeof(GIT_T));
    //update offset;
  } else {
    topElem[degree].n_docs += topElem[i].n_docs;
  }

  b->tableConsume += sizeof(GIT_T);
  return;
}

void checkIContent(int i){
  //Refill buffer of ioBufs[i]
  BUF_T *b = &ioBufs[i];

  if (b->contTotal - b->contConsume < sizeof(MIT_T)) {
    b->contTotal = fread(&(b->bufcont), (bufSize/sizeof(MIT_T)*sizeof(MIT_T)), 1, b->fcont);
    b->contConsume= 0;
  }

  if (b->tableTotal - b->tableConsume < sizeof(GIT_T)) {
    b->tableTotal = fread(&(b->buf), (bufSize/sizeof(GIT_T)*sizeof(GIT_T)), 1, b->f);
    b->tableConsume = 0;
  }

  return;
}

