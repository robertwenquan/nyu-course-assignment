#ifndef _tokenizer_h
#define _tokenizer_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Tokenizer type.  You need to fill in the type as part of your implementation.
 */

struct TokenizerT_ {
  char *delimiters;
  char *tokenStream;
  char **tokens;
  int numTokens;
  int numTokensDispensed;
};

typedef struct TokenizerT_ TokenizerT;

TokenizerT *TKCreate(char *separators, char *ts, int length);
char *TKGetNextToken(TokenizerT *tk);
void TKDestroy(TokenizerT *tk);
int isSpecialChar(char c);

#endif
