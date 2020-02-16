{-# LANGUAGE TemplateHaskell #-}
import Ex1

import Test.HUnit
import Data.List


-- mem x [] = False
-- mem x ((y,m):ys) = (x==y) || (mem x ys)

emptyEq :: ListBag Integer
emptyEq = empty

countOcc c [] = 0
countOcc c (x:xs) = if c == x then 1 + (countOcc c xs)
                  else countOcc c xs

_checkMul 0 s m = (countOcc (s!!0) s == mul (s!!0) m)
_checkMul i s m = (countOcc (s!!i) s == mul (s!!i) m) && _checkMul (i-1) s m

checkMul s m = _checkMul ((length s) - 1) s m

-- Basic sanity checks (BSC)
---- Well-formedness
testWfEmpty = TestCase $ assertBool "wf empty == True" (wf emptyEq)
testWfSingleton = TestCase $ assertBool "wf (singleton 42) == True" (wf (singleton 42))
testWfFromList = TestCase $ assertBool "wf (fromList \"abcdaad\") == True" (wf (fromList "abcdaad"))
testWfFail = TestCase $ assertBool "wf should return False" (wf (LB (replicate 2 (2,1))))

---- isEmpty
testIsEmptyE = TestCase $ assertBool "isEmpty empty == True" (isEmpty empty)

emptyLBFromList :: ListBag Int -- Needed to help the type reconstruction
emptyLBFromList = fromList []
testIsEmptyLE = TestCase $ assertBool "isEmpty (fromList []) == True" (isEmpty emptyLBFromList)
testIsEmptyST = TestCase $ assertEqual "isEmpty (singleton 42) == False" (isEmpty (singleton 42)) False
testIsEmptyLST = TestCase $ assertEqual "isEmpty (fromList [42]) == False" (isEmpty (fromList [42])) False
testIsEmptyFL = TestCase $ assertEqual "isEmpty (fromList [9,8,8,42,1,1]) == False" (isEmpty (fromList [9,8,8,42,1,1])) False

---- Multiplicity
testCheckMul = TestCase $ assertBool "checkMul \"abcdaad\" (fromList \"abcdaad\") == True" (checkMul "abcdaad" (fromList "abcdaad"))
testMulE = TestCase $ assertEqual "mul 5 (empty) == 0" (mul 5 (empty)) 0
testMulLE = TestCase $ assertEqual "mul 5 (fromList []) == 0" (mul 5 (fromList [])) 0
testMulST = TestCase $ assertEqual "mul 5 (singleton 5) == 1" (mul 5 (singleton 5)) 1
testMulLST = TestCase $ assertEqual "mul 5 (fromList [5]) == 1" (mul 5 (fromList [5])) 1
testMulLST3 = TestCase $ assertEqual "mul 5 (fromList [5,4,5,5]) == 3" (mul 5 (fromList [5,4,5,5])) 3
testMulLST0 = TestCase $ assertEqual "mul 42 (fromList [5,4,5,5]) == 3" (mul 42 (fromList [5,4,5,5])) 0
testMulSum0 = TestCase $ assertEqual "mul 96 (sumBag (fromList [1,5,2,78,42]) (fromList [1,55,98,42,42,42])) == 0" (mul 96 (sumBag (fromList [1,5,2,78,42]) (fromList [1,55,98,42,42,42]))) 0 
testMulSum4 = TestCase $ assertEqual "mul 42 (sumBag (fromList [1,5,2,78,42]) (fromList [1,55,98,42,42,42])) == 4" (mul 42 (sumBag (fromList [1,5,2,78,42]) (fromList [1,55,98,42,42,42]))) 4


---- FromList/ToList
testSort = TestCase $ assertEqual "sort (toList (fromList \"abcdaad\")) == sort \"abcdaad\"" (sort (toList (fromList "abcdaad"))) (sort "abcdaad")
testSumBag = TestCase $ assertEqual "sort (toList (sumBag (fromList \"abcdaad\") (fromList \"abcdaad\"))) == sort \"abcdaadabcdaad\"" (sort (toList (sumBag (fromList "abcdaad") (fromList "abcdaad")))) (sort "abcdaadabcdaad")

---- Properties of sum
testSumE = TestCase $ assertEqual "sumBag (fromList \"\") (fromList \"\") == (fromList \"\")" (sumBag (fromList "") (fromList "")) (fromList "")
testSumEUnit = TestCase $ assertEqual "sort (toList (sumBag empty (fromList \"helloworld\"))) == sort \"helloworld\"" (sort (toList (sumBag empty (fromList "helloworld")))) (sort "helloworld")

testWf = TestList [TestLabel "testWfEmpty" testWfEmpty,
                     TestLabel "testWfSingleton" testWfSingleton,
                     TestLabel "testWfFromList" testWfFromList]

testIsEmpty = TestList [TestLabel "testIsEmptyE" testIsEmptyE,
                        TestLabel "testIsEmptyLE" testIsEmptyLE,
                        TestLabel "testIsEmptyST" testIsEmptyST,
                        TestLabel "testIsEmptyLST" testIsEmptyLST,
                        TestLabel "testIsEmptyFL" testIsEmptyFL
                        ]
                        
testMul = TestList [TestLabel "testMulE" testMulE,            
                     TestLabel "testMulLE" testMulLE,
                     TestLabel "testMulST" testMulST,            
                     TestLabel "testMulLST" testMulLST,
                     TestLabel "testMulLST3" testMulLST3,            
                     TestLabel "testMulLST0" testMulLST0,
                     TestLabel "testMulSum0" testMulSum0,            
                     TestLabel "testMulSum4" testMulSum4]
                     
testLists = TestList [TestLabel "testSort" testSort,               
                     TestLabel "testSumBag" testSumBag]

testSum = TestList [TestLabel "testSumE" testSumE,               
                     TestLabel "testSumEUnit" testSumEUnit]


-- Main
main :: IO ()
main = do
  runTestTT testWf
  runTestTT testIsEmpty
  runTestTT testMul
  runTestTT testLists
  runTestTT testSum

  return ()
