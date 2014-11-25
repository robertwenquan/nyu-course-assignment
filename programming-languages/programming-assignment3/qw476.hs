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
import System.IO
import Data.List
import Text.Printf
import Data.IORef
import Data.String
import Data.Char
import Data.List
 

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
lower_bound :: Float -> Integer
lower_bound n = get_lower 0
  where
  get_lower :: Integer -> Integer
  get_lower x = if (fromIntegral (f (x+1))) >= n
                then
                  f x
                else
                  get_lower (x+1)

--
-- Define the higher bound function
--
upper_bound :: Float -> Integer
upper_bound n = get_upper 0
  where
  get_upper :: Integer -> Integer
  get_upper x = if n < (fromIntegral (f x))
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
  if name == "" then do
    printf "ERR\n"
    exitWith (ExitFailure 1)
  else do

  -- parse the command from readline
  let cmd_list = ["QUIT", "NTH", "SUM", "BOUNDS"]
  let cmd = (head (words name))

  -- check invalid command
  if (cmd `elem` cmd_list) == False then do
    printf "ERR\n"
    exitWith (ExitFailure 1)
  else do
    
  -- handle QUIT
  if cmd == "QUIT" then
    exitSuccess
  else do

  -- only one space is allowed between command and argument
  let space_cnt = length (' ' `elemIndices` name)
  if space_cnt > 1 then do
    printf "ERR\n"
    exitWith (ExitFailure 1)
  else do

  -- hanele non-QUIT commands with 0 arg or 1+ arg
  -- like BOUNDS
  -- or   BOUNDS 1 2
  if (length (words name)) /= 2 then do
    printf "ERR\n"
    exitWith (ExitFailure 1)
  else do
    
  let numstr = head (tail (words name))

  --
  -- NTH COMMAND
  --
  if cmd == "NTH" then do
    if all isNumber numstr /= True then do
      printf "ERR\n"
      exitWith (ExitFailure 1)
    else do

    let num = (read numstr :: Integer)

    if num < 0 then do
      printf "ERR\n"
      exitWith (ExitFailure 1)
    else do

    print (f num)

  --
  -- SUM COMMAND
  --
  else if cmd == "SUM" then do
    if all isNumber numstr /= True then do
      printf "ERR\n"
      exitWith (ExitFailure 1)
    else do

    let num = (read numstr :: Integer)

    if num < 0 then do
      printf "ERR\n"
      exitWith (ExitFailure 1)
    else do

    print (sumf num)

  --
  -- BOUNDS COMMAND
  --
  else if cmd == "BOUNDS" then do
    let num = (read numstr :: Float)

    if num <= 1 then do
      printf "ERR\n"
      exitWith (ExitFailure 1)
    else do

    printf "%d\n%d\n" (lower_bound num) (upper_bound num)

  else do
    -- never comes here!!
    printf "ERR\n"
    exitWith (ExitFailure 1)

  -- loop back
  main

