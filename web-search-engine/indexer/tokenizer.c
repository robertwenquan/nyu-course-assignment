/*
 * code from
 * https://github.com/alexandermtang/tokenizer/blob/master/tokenizer.c
 *
 * Changes:
 *  - add #ifdef __TEST__ for main()
 *  - add tokenizer.h
 *
 * Known Issues:
 *  - no buffer boundary with length limit
 *    with random string or unicode string passed in, it will work beyond
 *    the buffer boundary and destroy data after the buffer boundary
 */

# include "tokenizer.h"

/*
 * Alexander Tang and Craig Perkins
 * tokenizer.c
 */

// processes string, replaces "\n" with '\n' and '\0'
static char *preprocessString(char *str) {
  size_t length = strlen(str);
  int i;
  for (i = 0; i < length; i++) {
    if (str[i] == '\\') {
      switch (str[i+1]) {
        case 'n': str[i] = '\n'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case 't': str[i] = '\t'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case 'v': str[i] = '\v'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case 'b': str[i] = '\b'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case 'r': str[i] = '\r'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case 'f': str[i] = '\f'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case '\\': str[i] = '\\'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case 'a': str[i] = '\a'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
        case '"': str[i] = '\"'; memmove(str+i+1, str+i+2, strlen(str+i+1)*sizeof(char)); length--;
          break;
      }
    }
  }
  return str;
}

int isSpecialChar(char c) {
  return (c == '\n' || c == '\v' || c == '\t' || c == '\b' ||
      c == '\r' || c == '\f' || c == '\a' || c == '\"' || c == '\\');
}

/*
 * TKCreate creates a new TokenizerT object for a given set of separator
 * characters (given as a string) and a token stream (given as a string).
 *
 * TKCreate should copy the two arguments so that it is not dependent on
 * them staying immutable after returning.  (In the future, this may change
 * to increase efficiency.)
 *
 * If the function succeeds, it returns a non-NULL TokenizerT.
 * Else it returns NULL.
 *
 * You need to fill in this function as part of your implementation.
 */

TokenizerT *TKCreate(char *separators, char *ts) {
  size_t sepLength = strlen(separators) + 1; // +1 to include \0 at end of string
  size_t tsLength  = strlen(ts) + 1;

  TokenizerT *tokenizer  = (TokenizerT *)malloc(sizeof(TokenizerT));
  tokenizer->delimiters  = separators;
  tokenizer->tokenStream = ts;
  tokenizer->numTokens = 0;
  tokenizer->numTokensDispensed = 0;

  char *tempDelimiters  = (char *)calloc(sepLength, sizeof(char));
  strcpy(tempDelimiters, separators);

  char *tokenizedString = (char *)calloc(tsLength, sizeof(char));
  strcpy(tokenizedString, ts);

  tempDelimiters  = preprocessString(tempDelimiters);
  tokenizedString = preprocessString(tokenizedString);

  tsLength = strlen(tokenizedString);

  // replace delimiters with '\0'
  int i = 0;
  for (i = 0; i < sepLength; i++) {
    if (tempDelimiters[i] == '\0') {
      continue;
    }

    int j;
    for(j = 0; j < tsLength; j++) {
      if (tokenizedString[j] == tempDelimiters[i]) {
        tokenizedString[j] = '\0';
      }
    }
  }

  // get number of tokens
  char *ptr = tokenizedString;
  for (i = 0; i < tsLength + 1; i++) {
    while (*ptr == '\0') {
      ptr++;
      i++;
    }
    if (tokenizedString[i] == '\0') {
      tokenizer->numTokens++;
      ptr+=strlen(ptr);
    }
  }

  // malloc pointers depending on number of tokens
  tokenizer->tokens = (char **)calloc(tokenizer->numTokens, sizeof(char*));

  // assign tokens to tokenizer->tokens[i], with dynamically allocated memory for each token
  ptr = tokenizedString;
  int j = 0;
  for (i = 0; i < tsLength + 1; i++) {
    while (*ptr == '\0') {
      ptr++;
      i++;
    }
    if (tokenizedString[i] == '\0') {
      (tokenizer->tokens)[j] = (char *)malloc((strlen(ptr) + 1) * sizeof(char));
      strcpy((tokenizer->tokens)[j], ptr);
      ptr+=strlen(ptr);
      j++;
    }
  }

  free(tokenizedString);
  free(tempDelimiters);

  return tokenizer;
}

/*
 * TKDestroy destroys a TokenizerT object.  It should free all dynamically
 * allocated memory that is part of the object being destroyed.
 *
 * You need to fill in this function as part of your implementation.
 */

void TKDestroy(TokenizerT *tk) {
  int i;
  for (i = 0; i < tk->numTokens; i++) {
    free((tk->tokens)[i]);
  }
  free(tk->tokens);
  free(tk);
}

/*
 * TKGetNextToken returns the next token from the token stream as a
 * character string.  Space for the returned token should be dynamically
 * allocated.  The caller is responsible for freeing the space once it is
 * no longer needed.
 *
 * If the function succeeds, it returns a C string (delimited by '\0')
 * containing the token.  Else it returns 0.
 *
 * You need to fill in this function as part of your implementation.
 */

char *TKGetNextToken(TokenizerT *tk) {
  if (tk->numTokensDispensed < tk->numTokens) {
    return (tk->tokens)[tk->numTokensDispensed++];
  } else {
    return 0;
  }
}

/*
 * main will have two string arguments (in argv[1] and argv[2]).
 * The first string contains the separator characters.
 * The second string contains the tokens.
 * Print out the tokens in the second string in left-to-right order.
 * Each token should be printed on a separate line.
 */

#ifdef __TEST_TOKENIZER_
int main(int argc, char **argv) {
  if (argc < 3) {
    fprintf(stderr, "Too few => error\n");
    return -1;
  } else if (argc > 3) {
    fprintf(stderr, "Too many => error\n");
    return -1;
  }

  TokenizerT *tokenizer;
  tokenizer = TKCreate(argv[1], argv[2]);

  char *token;
  while ( (token = TKGetNextToken(tokenizer)) ) {
    size_t length = strlen(token);

    int i;
    for (i = 0; i < length; i++) {
      char c = token[i];
      if (isSpecialChar(c)) {
        printf("[0x%.2x]", c);
      } else {
        printf("%c", c);
      }
    }

    printf("\n");
  }

  TKDestroy(tokenizer);
  return 0;
}
#endif

