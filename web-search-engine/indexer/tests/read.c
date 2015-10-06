#include<stdio.h>
#include"../utils.h"

int main(){
  FILE * f;
  f = fopen("../test_data/phase3_output/input3.warc.mit", "r");
  MIT_T *buffer;
  buffer = (MIT_T*)malloc(sizeof(MIT_T));
  int total = 0;
  int zero = 0;
  while(!feof(f)){
    fgets(buffer, sizeof(MIT_T), f);
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
