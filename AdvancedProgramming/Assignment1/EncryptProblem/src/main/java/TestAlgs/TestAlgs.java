/*
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
 */

package TestAlgs;

import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

/**
 * Exercise 1.1 of AdvancedProgramming 2019.
 * Main class
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public class TestAlgs {    
    
    public static void main(String args[]) {
        
        /* If there were no arguments given, exit */
        if(args.length < 1) {
            System.err.println("Usage: parent directory to analyze.\nNo arguments were given. Exiting..");
            return;
        }
        
        /* Otherwise get the first parameter */
        String arg = args[0];
        Algs testAlgs = new Algs(arg) {
            
            @Override
            protected Pair<Method, Method> searchMethods(Class f, Method[] methods) {
                Method enc = null, dec = null;
        
                /* Look at each retrieved method */
                for(Method m : methods) {

                    /* If it starts with "enc" and has a parameter String, save this method for future uses */
                    if (m.getName().startsWith("enc")) 
                        enc = getMethodIfString(m);
                    
                    /* Same happens for the "dec" method.. */
                    else if (m.getName().startsWith("dec"))
                        dec = getMethodIfString(m);
                    
                }

                /*  The form of the class name is crypto.algos.NAME, to print NAME 
                *   just remove the first 13 chars (f.getName().substring(13)) or, 
                *   more generally, remove the parts before the last dot */
                System.out.println(f.getName().substring(f.getName().lastIndexOf(".") + 1));

                return new Pair(enc, dec);
            }
        };
        
        KeyRegistry kr = new KeyRegistry();
        
        /* Actual exercise */
        try {
            testAlgs.populateKeyRegistry(kr);
            testAlgs.solveExercise(kr);
        }
        catch(IOException | ClassNotFoundException | IllegalAccessException | 
                InvocationTargetException | InstantiationException | NoSuchMethodException e) {
            System.err.println(e.getMessage());
        }
    }
}

