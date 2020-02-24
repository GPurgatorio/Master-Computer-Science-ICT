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
import java.lang.annotation.Annotation;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;


/**
 * Optional exercise 1.2 of AdvancedProgramming 2019.
 * Main class
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public class TestAlgsPlus {
    
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
                    
                    /* If it starts with "enc".. */
                    if (m.getName().startsWith("enc"))
                        /* .. and has a parameter String */
                        enc = getMethodIfString(m);                        
                    
                    /* Same happens for the "dec" method.. */
                    else if (m.getName().startsWith("dec"))
                        dec = getMethodIfString(m);
                }
                
                /* If enc or dec aren't set yet, we look for annotations 
                *  in order to enrich the previous exercise with more
                *  possible methods.
                */
                if(enc == null || dec == null) {
                    
                    boolean encCheck = false, decCheck = false;
                    
                    for(Method m : methods) {

                        Annotation[] a = m.getAnnotations();

                        for(Annotation x : a) {

                            /* This is to check that there's EXACTLY ONE method with name "Encrypt" */
                            if (x.annotationType().getSimpleName().equals("Encrypt")) {
                                /* Since it's EXACTLY ONE, we check we haven't already put one with annotations */
                                if(encCheck) 
                                    enc = null;

                                else { /* Of course, we're still checking if it requires one String */
                                    enc = getMethodIfString(m);
                                    if(enc != null)
                                        encCheck = true;
                                }

                            }
                            /* And again the same happens for the "Decrypt" annotation .. */
                            else if (x.annotationType().getSimpleName().equals("Decrypt")) {
                                if(decCheck) 
                                    dec = null;

                                else {
                                    dec = getMethodIfString(m);
                                    if(dec != null)
                                        decCheck = true;
                                }
                            }
                        }
                    }
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