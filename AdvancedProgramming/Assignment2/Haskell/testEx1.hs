{-# LANGUAGE TemplateHaskell #-}
import Ex1

import Test.HUnit
import Data.List


mem x [] = False
mem x ((y,m):ys) = (x==y) || (mem x ys)

emptyEq :: ListBag Integer
emptyEq = empty

countOcc c [] = 0
countOcc c (x:xs) = if c == x then 1 + (countOcc c xs)
                  else countOcc c xs

_checkMul 0 s m = (countOcc (s!!0) s == mul (s!!0) m)
_checkMul i s m = (countOcc (s!!i) s == mul (s!!i) m) && _checkMul (i-1) s m

checkMul s m = _checkMul ((length s) - 1) s m

-- Actual tests
testWfEmpty = TestCase $ assertBool "wf empty == True" (wf emptyEq)
testWfSingleton = TestCase $ assertBool "wf (singleton 42) == True" (wf (singleton 42))
testWfFromList = TestCase $ assertBool "wf (fromList \"abcdaad\") == True" (wf (fromList "abcdaad"))
testWfFail = TestCase $ assertBool "wf should return False" (wf (LB (replicate 2 (2,1))))
testMul = TestCase $ assertEqual "mul 5 (singleton 5) == 1" (mul 5 (singleton 5)) 1
testCheckMul = TestCase $ assertBool "checkMul \"abcdaad\" (fromList \"abcdaad\") == True" (checkMul "abcdaad" (fromList "abcdaad"))
testSort = TestCase $ assertEqual "sort (toList (fromList \"abcdaad\")) == sort \"abcdaad\"" (sort (toList (fromList "abcdaad"))) (sort "abcdaad")
testSumBag = TestCase $ assertEqual "sort (toList (sumBag (fromList \"abcdaad\") (fromList \"abcdaad\"))) == sort \"abcdaadabcdaad\"" (sort (toList (sumBag (fromList "abcdaad") (fromList "abcdaad")))) (sort "abcdaadabcdaad")

testlist = TestList [TestLabel "testWfEmpty" testWfEmpty,
                     TestLabel "testWfSingleton" testWfSingleton,
                     TestLabel "testWfFromList" testWfFromList,             
                     TestLabel "testMul" testMul,            
                     TestLabel "testCheckMul" testCheckMul,               
                     TestLabel "testSort" testSort,               
                     TestLabel "testSumBag" testSumBag                 
                    ]

-- Main
main :: IO ()
main = do
  runTestTT testlist
  return ()
