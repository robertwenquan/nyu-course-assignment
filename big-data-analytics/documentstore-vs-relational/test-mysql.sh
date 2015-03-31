#!/bin/bash

for n in 100 1000 10000 100000 1000000
do
  infile="test/load-${n}.sql"
  echo "Executing $infile"
  time mysql -u qw476 -uqw476123 test < $infile
#  echo "Test query"
#  time mysql -u qw476 -uqw476123 test < test/query.sql >/dev/null
#  echo "Test update"
#  time mysql -u qw476 -uqw476123 test < test/update.sql
  echo "Complex query"
  time mysql -u qw476 -uqw476123 test < test/complex.sql >/dev/null

  echo "Test delete"
  time mysql -u qw476 -uqw476123 test < test/delete.sql
done

