--     ********************************************************
--     * Programming Language Fall 2015                       *
--     *   Programming Assignment 2                           *
--     *                                                      *
--     *   Caicai CHEN                                        *
--     *     caicai.chen@nyu.edu                              *
--     *     NetId: cc4584                                    *
--     ********************************************************

import System.IO
import System.Exit
import Text.Printf
import Data.Char
import Data.List

-- NTH Calculation
mem_f :: Int -> Integer
mem_f = (map f [0 ..] !!)
  where f  0 = 1
        f  1 = 1
        f  2 = 1
        f  3 = 1
        f  n = (mem_f(n-1)+mem_f(n-2))*mem_f(n-3) `div` mem_f(n-4)

-- UPPER BOUND
-- Find the first larger number accoding to upperBound place
upperBound :: Int -> Double -> Integer
upperBound m n
  | fromIntegral(mem_f(m)) <= n  =  upperBound (m+1) n
  | otherwise = mem_f(m)

-- LOWER BOUND
-- Find the first smaller number accoding to upperBound place
lowerBound :: Int -> Double -> Integer
lowerBound m n
  | fromIntegral(mem_f(m)) < n = lowerBound (m+1) n
  | otherwise = mem_f(m-1)

-- SUM
getSum :: Int -> Integer
getSum n
  | n == 0  = 1
  | otherwise = mem_f(n) + getSum (n-1)


main = do 

  -- Exit Success if "end of file" seen
  eof <- isEOF
  if (eof == True ) then do
    exitWith (ExitSuccess)
  else do 

  inputStr <- getLine

  -- Empty input
  if (inputStr == "") then do
    printf "ERR\n"
    exitWith (ExitFailure 1)
  else do

  -- NO WS in the head
  if (head inputStr == ' ') then do
    printf "ERR\n"
    exitWith (ExitFailure 2)
  else do

  -- NO WS in the end
  if (last inputStr == ' ') then do
    printf "ERR\n"
    exitWith (ExitFailure 3)
  else do

  -- GET COMMAND
  let command = head (words inputStr)

  -- Deal with "QUIT"
  if (command == "QUIT") then do
    if ((length(inputStr)) > 4) then do
      printf "ERR\n"
      exitWith (ExitFailure 4)
    else do
      exitWith (ExitSuccess)
  else do

  -- Exit if not exactly 1 argument after command
  if ( length (words inputStr) /= 2) then do
    printf "ERR\n"
    exitWith (ExitFailure 5)
  else do

  let number = (last (words inputStr))
  
  -- Deal with "NTH"
  if (command == "NTH") then do
    if (all isDigit(number)) == False then do
      printf "ERR\n"
      exitWith (ExitFailure 6)
    else do
      let num = (read number :: Int)
      printf "%d\n" (mem_f(num)) 

  -- Deal with "SUM"   
  else if (command == "SUM") then do 
    if (all isDigit(number)) == False then do
      printf "ERR\n"
      exitWith (ExitFailure 7)
    else do
      let num = (read number :: Int)
      printf "%d\n" (getSum(num)) 

  -- Deal with "BOUNDS"
  else if (command == "BOUNDS") then do

    -- At most one "." is allowed
    if (length ((findIndices( == '.') number)) > 1) then do
      printf "ERR\n"
      exitWith (ExitFailure 8)
    else do

    -- if number is leading with '.', means it less than 1
    if (head (number) == '.') then do
      printf "ERR\n"
      exitWith (ExitFailure 9)
    else do

    -- All char should be digit apart from '.'
    if ( all isDigit((snd (partition( `elem` ['.']) number))))==False then do
      printf "ERR\n"
      exitWith (ExitFailure 10)
    else do

    -- if number is end with '.', remove the point
    if (last (number) == '.') then do
      let strip = takeWhile(/='.') number
      let num = (read strip :: Double)
      if (num <= 1) then do
        printf "ERR\n"
        exitWith (ExitFailure 11)
      else do
        printf "%d\n" (lowerBound 3 num)
        printf "%d\n" (upperBound 3 num)
    else do

    let num = (read number:: Double)
    if (num <= 1) then do
      printf "ERR\n"
      exitWith (ExitFailure 12)
    else do
      printf "%d\n" (lowerBound 3 num)
      printf "%d\n" (upperBound 3 num)

  else do
    printf "ERR\n"
    exitWith (ExitFailure 13)

  main
