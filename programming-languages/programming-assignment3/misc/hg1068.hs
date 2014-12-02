import Data.Char
import Data.List
import Control.Monad
import Text.Read
import System.IO
import System.Exit

foo :: Int -> Integer
foo n = fibs !! n
    where fibs = 1 : 1 : 1 : 1 : zipWith4 (\w x y z -> ((w + x) * y) `div` z) (tail(tail(tail fibs))) (tail(tail fibs)) (tail fibs) fibs
{--
foo 0 = 1
foo 1 = 1
foo 2 = 1
foo 3 = 1
foo n = ((foo(n-1) + foo(n-2)) * foo(n-3)) `div` foo(n-4)
--}

nth :: Int -> Integer
nth n = foo n

summ :: Int -> Integer
summ 0 = 1
summ n = (foo n) + summ(n-1)

i :: Int
i = 1
upperbound :: Double -> Integer
upperbound n = upper i
     where
     upper :: Int -> Integer
     upper a
       | fromInteger (foo a) > n = foo a
       | otherwise   = upper (a+1)

lowerbound :: Double -> Integer
lowerbound n = lower 1
     where
     lower :: Int -> Integer
     lower a
       | (fromInteger (foo a)) > n && (fromInteger (foo (a-1))) /= n = foo(a-1)
       | fromInteger (foo a) > n && fromInteger (foo (a-1)) == n = foo(a-2)
       | otherwise                       = lower(a+1)


main = do
   ie <- isEOF
   if ie
      then do exitFailure
      else do return()
   input1 <- getLine
   if all isSpace input1 || null input1
      then do main
      else do let input1_sep = words input1
              let input1_cmd = head input1_sep
              if  input1_cmd == "NTH" && length input1_sep == 2
                       then do  let input1_para = last input1_sep
                                if  all isDigit input1_para && (read input1_para :: Int) >= 0
                                then do let result1 = nth (read input1_para :: Int)
                                        print result1
                                        main

                                else do putStrLn"ERR"

                       else if  input1_cmd == "SUM" && length input1_sep == 2
                                then do
                                     let input1_para = last input1_sep
                                     if  all isDigit input1_para && (read input1_para :: Int) >= 0
                                         then do let result2 = summ (read input1_para :: Int)
                                                 print result2
                                                 main
                                         else do putStrLn"ERR"

                                else if  input1_cmd == "BOUNDS" && length input1_sep == 2
                                         then do let input1_para = last input1_sep
                                                 case (readMaybe input1_para :: Maybe Double) of
                                                     Just f | f > 1.0 -> do
                                                                         let result3 = upperbound (read input1_para :: Double)
                                                                         let result4 = lowerbound (read input1_para :: Double)
                                                                         print result4
                                                                         print result3
                                                                         main
                                                            | otherwise -> do
                                                                           putStrLn"ERR"

                                                     Nothing -> do putStrLn"ERR"

                                         else if  input1_cmd == "QUIT"
                                                  then do return()
                                                  else do  putStrLn"ERR"
