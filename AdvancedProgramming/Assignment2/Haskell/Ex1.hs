{-
 * Copyright (C) 2019 Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
-}

-- Author: Giulio Purgatorio, 516292

{-  NOTE: The quoted comments ("like this one") are a copy-paste from instructions  -}

module Ex1 where


{-  "based on the following concrete Haskell definition of the ListBag type constructor:"   -}
data ListBag a = LB [(a, Int)]
  deriving (Show, Eq)

 
--    Constructors


{-  "1. empty, that returns an empty ListBag" -}
empty :: ListBag a
empty = LB []



{-  "2. singleton v, returning a ListBag containing just one occurrence of element v"   -}
singleton :: a -> ListBag a
singleton v = LB [(v,1)]



--  Auxiliary function to insert a value (v) in a ListBag
insertLB :: Eq a => a -> ListBag a -> ListBag a
insertLB v (LB []) = singleton v
insertLB v (LB ((x, n):xs))
  | v == x = LB ((x, n+1):xs)       -- If the element I'm trying to add is already present in the ListBag, I increase its occurrencies
  | xs == [] = LB [(x,n),(v,1)]     -- If it's not the precedent case and the list has no more items, insert the value with occurrencies = 1
  | otherwise = let LB rest = insertLB v (LB xs) in LB ((x, n):rest)



{-  "3. fromList lst, returning a ListBag containing all and only the elements of lst, each with the right multiplicity"    -}
fromList :: Eq a => [a] -> ListBag a
fromList lst = fromList' lst
  where
    fromList' [] = empty
    fromList' [x] = singleton x
    fromList' (x:xs) = let toList = fromList' xs in insertLB x toList


--    Operations 


{-  "the predicate wf that applied to a ListBag returns True if and only if the argument is well-formed"    -}
wf :: Eq a => ListBag a -> Bool
wf bag = wf' bag
  where
    wf' (LB []) = True
    wf' (LB ((x, n):xs)) = let rest = wf' (LB xs) in not (insideLB x (LB xs)) && rest



--  Auxiliary function to check if a value (v) is already present in the ListBag
insideLB :: Eq a => a -> ListBag a -> Bool
insideLB v (LB []) = False
insideLB v (LB ((x, n):xs))
  | x == v = True
  | otherwise = insideLB v (LB xs)



{-  "isEmpty bag, returning True if and only if bag is empty"   -}
isEmpty :: ListBag a -> Bool
isEmpty bag = case bag of
  LB [] -> True
  _ -> False



--  Auxiliary function to get the value of a given key (v) in a ListBag
getLB :: Eq a => a -> ListBag a -> Int
getLB v (LB((x, n):xs))
  | v == x = n
  | otherwise = let rest = getLB v (LB xs) in rest



{-  "mul v bag, returning the multiplicity of v in the ListBag bag if v is an element of bag, and 0 otherwise"  -}
mul :: Eq a => a -> ListBag a -> Int
mul v bag
  | insideLB v bag == False = 0
  | otherwise = getLB v bag



{-  "toList bag, that returns a list containing all the elements of the ListBag bag, each one repeated a number of times equal to its multiplicity" -}
toList :: ListBag a -> [a]
toList bag = toList' bag
  where
    toList' (LB []) = []
    toList' (LB ((x, n):xs)) = let rest = toList' (LB xs) in replicate n x ++ rest



{-  "sumBag bag bag', returning the ListBag obtained by adding all the elements of bag' to bag" -}
sumBag :: Eq a => ListBag a -> ListBag a -> ListBag a
sumBag bag bag' = fromList ((toList bag) ++ (toList bag'))

