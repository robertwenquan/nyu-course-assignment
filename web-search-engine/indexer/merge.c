#include<stdio.h>
#include<stdlib.h>
#include"utils.h"
typedef struct{
    FILE *f; 
    FILE *fcont;
    GIT_T* buf; 
    MIT_T* bufcont;
    int tableTotal; 
    int tableConsume;
    int contTotal;
    int contConsume;} buffer;

void MergeCont();
char* mergeFiles(char* inputlist, char* path, int numLevel);
char* testmergeFiles(char* inputlist, char* path, int numLevel);
void writeMin(int i);
int sortCurr(int degree);
buffer *ioBufs;
GIT_T *topElem;
int bufSize;
/**************************************************************************/
/* usage  ./merge maxdegree memsize finlist outfileprefix foutlist        */
/*                                                                        */
/*        maxdegree      : n-way merge                                    */
/*        memsize        : size of available memory in bytes              */
/*        finlist        : name of file containing a list of input files  */
/*        outfileprefex  : directory to record intermediate files         */
/*        foutlist       : name of file containing a list of output files */
/**************************************************************************/

int maxDegree;
int memSize;

int main(int argc, char* argv[]){
  maxDegree = atoi(argv[1]);
  memSize = atoi(argv[2]);

  FILE *fin;
  char filename[1024];

  int numFiles = 0;
  int numLevel = 0;
  int inputsize;

  char inputlist[1024];
  strcpy(inputlist, argv[3]);

  fin = fopen(inputlist, "r");
  if(fin == NULL)
    return -1;
  if(feof(fin)){
    fclose(fin);
    return -1;
  }

  for(inputsize = 0; !feof(fin) && inputsize<=1; inputsize++){
    fgets(filename, 1024, fin);
    if(feof(fin))
      break;
  }
  fclose(fin);

  while(inputsize-1){
    strcpy(inputlist, mergeFiles(inputlist, argv[4], numLevel));
    numLevel++;
    fin = fopen(inputlist, "r");

    for(inputsize = 0; !feof(fin) && inputsize<=1; inputsize++){
      fgets(filename, 1024, fin);
      if(feof(fin))
        break;
    }
    fclose(fin);
  }

  printf("%s is the output list\n",inputlist);
  return 0;
}

char* mergeFiles(char* inputlist, char* path, int numLevel){
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
  ioBufs = (buffer *)malloc((maxDegree + 1) * sizeof(buffer));

  sprintf(outlist, "%s%d", path, numLevel);
  fin = fopen(inputlist, "r");
 
  while(!feof(fin)){
    //Get source files from the list, assign each file to a BUFFER structure
    for(degree = 0; degree < maxDegree; degree++){
      fscanf(fin, "%s", filename);
      if(feof(fin))
        break;
      ioBufs[degree].f = fopen(filename, "r");
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

    bufSize = memSize / (degree*3);

    for(i = 0; i <= degree; i++){
      ioBufs[i].buf = &(bufSpace[ i * bufSize * 2]);
      ioBufs[i].bufcont = &(bufSpace[ i * bufSize * 2 + bufSize / 2 ]);
      ioBufs[i].tableTotal = 0;
      ioBufs[i].tableConsume = 0;
      ioBufs[i].contTotal = 0;
      ioBufs[i].contConsume = 0;
    }
    ioBufs[degree].bufcont = &(bufSpace[ degree * bufSize * 2 + bufSize * degree/ 4 ]);

    mergeCont(degree);

    for(i = 0; i <= degree; i++){
      fclose(ioBufs[i].f);
      fclose(ioBufs[i].fcont);
    }

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

void getNextWord(int i){
  if(i == -1){
    return;
  }
  buffer *b = &(ioBufs[i]);

  if(b->tableConsume == b->tableTotal){
    b->tableTotal = fread(&(b->buf), (bufSize/sizeof(GIT_T)*sizeof(GIT_T)), 1, b->f);
    b->tableConsume = 0;  
  }

  if(b->tableTotal == 0){
    topElem[i].word_id = -1;
    return;
  }

  memcpy(&topElem[i], &(b->buf[b->tableConsume]), sizeof(GIT_T));
  b->tableConsume += sizeof(GIT_T);

  return;
}

int mergeCont(int degree){
  GIT_T *lastRecord;
  topElem = (GIT_T *)malloc(sizeof(GIT_T) * degree);

  int i;
  for(i = 0; i < degree - 1; i++){
    getNextWord(i);
  }
 
  int min = 0;
  while( min >= 0 ){
    min = sortCurr(degree-1);
    writeMin(min);
    getNextWord(min);
  } 
  return 0;
}

int sortCurr(int degree){
  int minPos = -1;
  int i;
  for(i = 0; i < degree; i++){
    if(topElem[i].word_id != -1){
      if(minPos == -1){
        minPos = i;
      }else if(topElem[i].word_id < topElem[minPos].word_id){
        minPos = i;
      }
    }
  }
  return minPos;
}

void writeMin(int i){
  if(i == -1){
    //flush everything to disk
  }
  buffer *b = &ioBufs[i];
  //write b->fcont
  //if topElem[i].word_id is different with topElem[degree], then write topElem[degree] to output file and update topElem[degree], if they are the same, update topElem[degree].n_docs
  return;
}
