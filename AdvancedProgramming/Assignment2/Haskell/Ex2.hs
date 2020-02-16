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

module Ex2 where

import Ex1


instance Foldable ListBag where
   foldr f z (LB []) = z
   foldr f z (LB ((x, n):xs)) = x `f` foldr f z (LB xs)

   
-- Auxiliary constructor to not insert n-1 times into the mapLB
manyton :: Eq a => a -> Int -> ListBag a
manyton v n = fromList (take n (cycle [v]))


-- "returns the ListBag of type b obtained by applying f 
--      to all the elements of its second argument."
mapLB :: (Eq a1, Eq a2) => (a1 -> a2) -> ListBag a1 -> ListBag a2
mapLB f (LB []) = empty
mapLB f (LB ((x, n):xs))
    | xs == [] = manyton (f x) n
    | otherwise = sumBag (manyton (f x) n) (mapLB f (LB xs))


-- Example function to use with mapLB
doubleValue :: Num a => a -> a
doubleValue a = a * 2

{-
Check it with:
    let a = fromList [1,2,3,4,2,3,2,4,5]
    mapLB doubleValue a
    
    will print a with all the keys doubled and leave the multiplicities unchanged
-}


{-
    Part 3:
    "Explain (in a comment in the same file) why it is not possible to 
    define an instance of Functor for ListBag by providing mapLB as 
    the implementation of fmap."
    
    From:           https://wiki.haskell.org/Functor
    
        "Functors are required to obey certain laws in regards to their mapping. 
        Ensuring instances of Functor obey these laws means the behaviour of fmap remains predictable"
        
        1) Functors must preserve identity morphisms
            fmap id = id
        2) Functors preserve composition of morphisms
            fmap (f . g)  ==  fmap f . fmap g
        
    Answer:
        
        Looking online was very helpful to learn a lot of things about Haskell. 
        We can see in this stackoverflow thread
            ( https://stackoverflow.com/questions/8305949/haskell-functor-implied-law/8323243#8323243 )
        
        "Given fmap id = id, fmap (f . g) = fmap f . fmap g follows from the free theorem for fmap."
            (proof: https://github.com/quchen/articles/blob/master/second_functor_law.md )
            
        This implies that only the first one has to be checked, which at first look seems like it's a straight-forward
        and obvious thing, while the second one may be the tough one. This happens everytime we're assuming no "bottom"
        is involved (otherwise we can get to the opposite consideration, as stated in the same repo).
        "Bottom" refers to a compilation which never completes successfully.
        
        So assuming we aren't in a "bottom" situation, our 
            fmap id = return 
        will do the trick, so we're looking at the second law about composition.
        
        instance Functor ListBag where
            fmap f (LB []) = empty
            fmap f (LB a) = mapLB f (LB a)
            
        but since we're talking about Eq types (due to our checks on the values in the (x, n) pairs composing the LB)
        this is not allowed.
        
        Otherwise, one case may be simply to have "undefined" and then the first law becomes invalid by simply choosing
        f = undefined
        
-}
