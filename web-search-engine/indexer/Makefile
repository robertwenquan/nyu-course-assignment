#
# Makefile for iigen
#

CC = gcc
CFLAGS = -g -O2 -Wall

OBJS = iigen.o lexicon.o iindex.o utils.o warc.o merge.o
BINS = iigen lexicon_gen iindex_gen iindex_merge

all:  $(BINS)

iigen:  $(OBJS)

lexicon_gen:  lexicon.c
	$(CC) $(CFLAGS) -D__TEST__ -o $@ $<

iindex_gen:  iindex.c
	$(CC) $(CFLAGS) -D__TEST__ -o $@ $<

iindex_merge:  merge.c
	$(CC) $(CFLAGS) -D__TEST__ -o $@ $<

clean:  
	rm -fr $(BINS) $(OBJS) iigen.dSYM *.pyc tests/*.pyc &>/dev/null

