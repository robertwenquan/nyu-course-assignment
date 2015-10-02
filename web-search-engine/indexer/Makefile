#
# Makefile for rigen
#

CC = gcc
CFLAGS = -g -O2
OBJS = rigen.o lexicon.o rindex.o utils.o
BINS = rigen lexicon_gen rindex_gen

all:  $(BINS)

rigen:  $(OBJS)

lexicon_gen:  lexicon.c
	$(CC) -D__TEST__ -o $@ $<

rindex_gen:  rindex.c
	$(CC) -D__TEST__ -o $@ $<

clean:  
	rm -fr $(BINS) $(OBJS) rigen.dSYM &>/dev/null

