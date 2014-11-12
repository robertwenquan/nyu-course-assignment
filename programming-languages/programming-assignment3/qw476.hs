------------------------------------------------------------------------
---- Programming Language Class Fall 2014 Semester
----   Programming Assignment 3
----
----   Quan Wen (robert.wen@nyu.edu) | netid: qw476
----
----   $Id$
------------------------------------------------------------------------


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
--  putStrLn("wwwwww")
--  name <- getLine
--  putStrLn("Hello, World " ++ name ++ "!")
-------------------------------------------

  let x = 7
  let y = f 4
  let z1 = sumf 4
  let z2 = lower_bound 16
  let z3 = upper_bound 16

  print y
  print z1
  print z2
  print z3

