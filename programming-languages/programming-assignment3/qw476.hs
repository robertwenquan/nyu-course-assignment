------------------------------------------------------------------------
---- Programming Language Class Fall 2014 Semester
----   Programming Assignment 3
----
----   Quan Wen (robert.wen@nyu.edu) | netid: qw476
----
----   $Id$
------------------------------------------------------------------------

import Control.Monad
import Control.Arrow
import System.Exit
import Data.List
import Text.Printf
import Data.IORef
import Data.String
import System.IO
 

--
-- Define the f function
--
f :: Integer -> Integer
f 0 = 1
f 1 = 1
f 2 = 1
f 3 = 1
f n = (f (n-1) + f (n-2)) * f (n-3) `div` f (n-4)


--
-- Define the sumf function
--
sumf ::  Integer -> Integer
sumf 0 = 1
sumf n = f (n) + sumf (n-1)


--
-- Define the lower bound function
--
lower_bound :: Integer -> Integer
lower_bound n = get_lower 0
  where
  get_lower :: Integer -> Integer
  get_lower x = if f (x+1) >= n
                then
                  f x
                else
                  get_lower (x+1)

--
-- Define the higher bound function
--
upper_bound :: Integer -> Integer
upper_bound n = get_upper 0
  where
  get_upper :: Integer -> Integer
  get_upper x = if n < f x
                then
                  f x
                else
                  get_upper (x+1)


main = do

-------- Input and Output Examples --------

  -- detect EOF and exit silently
  end_of_file <- isEOF
  if end_of_file then
    exitSuccess
  else do

  -- read one line from STDIN
  name <- getLine

  -- parse the command from readline
  let cmd_list = ["QUIT", "NTH", "SUM", "BOUNDS"]
  let cmd = (head (words name))

  -- check invalid command
  if (cmd `elem` cmd_list) == False then do
    printf "ERR\n"
    exitWith (ExitFailure 1)
  else if cmd == "QUIT" then
    exitSuccess
  else do

  let num = (read (head (tail (words name))) :: Integer)

  if num < 0 then do
    printf "ERR\n"
    exitWith (ExitFailure 1)
  else do

  if cmd == "NTH" then do
    print (f num)
  else if cmd == "SUM" then do
    print (sumf num)
  else if cmd == "BOUNDS" then do
    if num == 1 then do
      printf "ERR\n"
      exitWith (ExitFailure 1)
    else
      printf "%d\n%d\n" (lower_bound num) (upper_bound num)
  else do
    -- never comes here!!
    printf "ERR\n"
    exitWith (ExitFailure 1)

  main

