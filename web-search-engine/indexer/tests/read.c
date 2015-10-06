#include<stdio.h>
#include"../utils.h"

int main(int argc, char* argv[]){
  FILE * f;
  f = fopen(argv[1], "r");
  MIT_T *buffer;
  buffer = (MIT_T*)malloc(sizeof(MIT_T));
  int total = 0;
  int zero = 0;
  while(!feof(f)){
    fread(buffer, sizeof(MIT_T),1, f);
    printf("%d\n", buffer[0].docid);
    printf("%d\n", buffer[0].offset);
    printf("%d\n", buffer[0].n_places);
    printf("%s\n","");
    if(buffer[0].n_places == 0)
      zero++;
    total++;
  }
  printf("there are %d entries ", total);
  printf("%d is zero", zero);
  return 0;
}
