#
# Makefile for iigen
#

UNAME := $(shell uname)

CC = gcc
ifeq ($(UNAME), Linux)
CFLAGS = -g -O2 -Wall -D__DEBUG__ -D__LINUX__
else
CFLAGS = -g -O2 -Wall -D__DEBUG__ -D__MACOS__
endif

OBJS = iigen.o lexicon.o iindex.o utils.o warc.o merge.o tokenizer.o
BINS = iigen lexicon_gen iindex_gen iindex_merge

all:  $(BINS)

iigen:  $(OBJS)

lexicon_gen:  lexicon_test.o warc_test.o tokenizer.o utils.o
	$(CC) -o $@ lexicon_test.o warc_test.o tokenizer.o utils.o

lexicon_test.o:  lexicon.c
	$(CC) -c $(CFLAGS) -D__TEST__ -o $@ $<

warc_test.o:  warc.c
	$(CC) -c $(CFLAGS) -D__TEST__ -o $@ $<

tokenizer.o:  tokenizer.c
	$(CC) -c $(CFLAGS) -D__TEST__ -o $@ $<

utils.o:  utils.c
	$(CC) -c $(CFLAGS) -D__TEST__ -o $@ $<

iindex_gen:  iindex.c
	$(CC) $(CFLAGS) -D__TEST__ -o $@ $<

iindex_merge:  merge.c
	$(CC) $(CFLAGS) -D__TEST__ -o $@ $<

clean:  
	rm -fr $(BINS) $(OBJS) *.dSYM *.pyc tests/*.pyc *.o &>/dev/null

