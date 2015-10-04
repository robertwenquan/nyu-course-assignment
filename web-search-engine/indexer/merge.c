#include<stdio.h>
#include<stdlib.h>

typedef struct{
    FILE *f; 
    FILE *fcont;
    char* buf; 
    char* bufcont;
    int start; 
    int end;} buffer;
typedef struct{int wordid; int place;} wordinfo;

void MergeCont();
char* mergeFiles(char* inputlist, char* path, int numLevel);
char* testmergeFiles(char* inputlist, char* path, int numLevel);
buffer *ioBufs;

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

  printf("%s is the ",inputlist);
  return 0;
}

char* testmergeFiles(char* inputlist, char* path, int numLevel){
    FILE* fout;
    
    char filename[1024];
    sprintf(filename, "%s%d", "output", numLevel);
    fout = fopen(filename, "w");
    int i;
    for(i = 0; i < 3-numLevel; i++){
      fprintf(fout, "%s\n", "abc");
    }
    fclose(fout);
    return filename;
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
  wordinfo *heap;
  heap = (wordinfo *)malloc((maxDegree+1)*sizeof(wordinfo));

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

    bufSize = memSize / (degree*3);

    for(i = 0; i < degree; i++){
      ioBufs[i].buf = &(bufSpace[ i * bufSize * 2]);
      ioBufs[i].bufcont = &(bufSpace[ i * bufSize * 2 + bufSize / 2 ]);
    }

    mergeCont();

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

//wordinfo* getInfo(int i)

int mergeCont(){
  //int degree;
  //for(degree = 0; degree < maxDegree; degree++){

  //}
  //  for(i = 0; i < degree; i++)
  //    heap[i+1] = getInfo(i);
  return 0;
}


