#
# Makefile for iigen
#

UNAME := $(shell uname)

CC = gcc
ifeq ($(UNAME), Linux)
CFLAGS = -g -O2 -Wall -D__DEBUG__ -D__LINUX__
else
CFLAGS = -g -O2 -Wall -D__DEBUG__ -D__MACOS__ -I /usr/local/Cellar/libyaml/0.1.6_1/include
endif

OBJS = query.o word_search.o doc_search.o iindex_search.o utils.o pagerank.o page_search.o
BINS = search

all:  $(BINS)

search:  $(OBJS)
	$(CC) -o $@ $(OBJS) -lm

clean:  
	rm -fr $(BINS) $(OBJS) *.dSYM *.pyc tests/*.pyc *.o &>/dev/null

