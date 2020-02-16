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

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;
import java.util.Set;

/**
 * Abstract class to exploit code reuse in Exercise 1.1 and 1.2 of the
 * Advanced Programming's course of Pisa's University (2019-2020).
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public abstract class Algs {
    
    /* The directory where to find all the files (will be concatenated with /crypto) */
    private final String arg;
    private ClassLoader cl;
    
    
    /**
     * Constructor.
     * @param directory the parent directory of crypto
     */
    public Algs(String directory) {
        /*  Concatenate a '/' at the end (if there's not one) */
        if (!directory.endsWith("/"))
            directory = directory.concat("/");
        /* and enter into the main directory of the assignment */
        arg = directory;
    }
    
    
    /**
     * Init code that is being shared by both exercises (1.1 and 1.2).
     * 
     * @param kr the KeyRegistry to populate
     * @return a KeyRegistry
     * @throws FileNotFoundException
     * @throws IOException
     * @throws ClassNotFoundException 
     */
    protected final KeyRegistry populateKeyRegistry(KeyRegistry kr) 
            throws FileNotFoundException, IOException, ClassNotFoundException {
        
        File dir = new File(arg + "crypto");
        
        /* Get the URL to be passed to the ClassLoader */
        URL[] classLoaderUrls = new URL[]{new File(arg).toURI().toURL()};

        /* Create the classLoader that will load the various classes */
        cl = new URLClassLoader(classLoaderUrls);

        /* Instantiate a new KeyRegistry, as defined in the assignment */
        if (kr == null) 
            kr = new KeyRegistry();

        /* And open the keys.list file */ 
        try (BufferedReader br = new BufferedReader(new FileReader(new File(dir + "/keys.list")))) {
            
            String w;
            /* Read from keys.list (name "w" is because of the later part of the assignment) */
            while ((w = br.readLine()) != null) {
                /* The entries are pair (NameOfAlgo IntegersWithCommas), so split it on a space */
                int spaceIndex = w.indexOf(" ");
                
                /* The class is the first part of the split */
                String className = w.substring(0, spaceIndex);
                Class classToLoad = cl.loadClass(className);
                
                /* And adds it to the KeyRegistry, with value as the 2nd part of the split */
                kr.add(classToLoad, w.substring(spaceIndex + 1));
            }
        }
        return kr;
        
    }
    
    
    /**
     * Code that is being shared by both exercises (1.1 and 1.2).
     * 
     * @param kr the KeyRegistry with the loaded data
     * @throws NoSuchMethodException
     * @throws ClassNotFoundException
     * @throws IllegalAccessException
     * @throws IllegalArgumentException
     * @throws InvocationTargetException
     * @throws InstantiationException
     * @throws IOException 
     */
    protected void solveExercise(KeyRegistry kr) 
            throws NoSuchMethodException, ClassNotFoundException, IllegalAccessException, 
                IllegalArgumentException, InvocationTargetException, InstantiationException, IOException {
        
        /* Get all the keys that were added to the class.. */
        Set<Class> keys = kr.getKeys();

        /* .. in order to iterate on them */
        for(Class f : keys) {

            /* Get the name of the previously saved class */
            String className = f.getName();

            /* Load the class */
            Class classToLoad = cl.loadClass(className);

            /* Get its constructor (which requires a String argument) */
            Constructor<?> constructor = classToLoad.getConstructor(String.class);
            
            if(constructor == null) {
                System.out.println("Enc/Dec methods not found");
                continue;
            }

            /* Get its methods in order to check if there are the methods starting with "enc" and "dec" */
            Method[] methods = classToLoad.getDeclaredMethods();
            Pair<Method, Method> foundEncDec = searchMethods(f, methods);
            
            if(!foundEncDec.bothNotNull()) {
                System.out.println("Enc/Dec methods not found");
                continue;
            }
            
            Method enc = foundEncDec.first;
            Method dec = foundEncDec.second;
            
            /* So we get its previously stored value in the KeyRegistry */
            String values = kr.get(f);
            String w;
                
            /* Read the file. Name of Strings are specified in the assignment's requests */
            /* And open the file "secret.list" */
            try (BufferedReader br = new BufferedReader(new FileReader(new File(arg + "crypto/secret.list")))) {
                
                /* Read the file. Name of Strings are specified in the assignment's requests */
                while ((w = br.readLine()) != null) {
                    /* Instantiate a new object with the constructor we got earlier */
                    Object o = constructor.newInstance(values);
                    
                    /* And invoke the encryption algorithm on the string */
                    String e = (String) enc.invoke(o, w);
                    /* Then decrypt the result */
                    String d = (String) dec.invoke(o, e);
                    
                    /* And check if the returned value is the same of what it was originally passed */
                    if(!d.equals(w)) {
                        
                        /* The word might have paddings, which means that it is in the form of d = w##..# */
                        d = d.replaceAll("#", "");
                        
                        if(!d.equals(w))
                            System.out.println("KO: " + w + " -> " + e + " -> " + d);
                    }
                }
            }
        }
    }
    
    
    /** 
     * Implemented in TestAlgs for Exercise 1.1 and TestAlgsPlus for Exercise 1.2.
     * Depending on the Exercise the way to choose the methods "Enc" and "Dec"
     * may differ, so it's left to be implemented in the actual exercise.
     * 
     * @param f the class that is being checked
     * @param methods the methods of the class
     * @return a pair of methods, in order: Enc method, Dec method
    */
    protected abstract Pair<Method, Method> searchMethods(Class f, Method[] methods);
    
    
    /**
     * Returns the given Method if and only if that method requires one String as parameter.
     * @param m the method to be checked
     * @return the method or null
     */
    protected Method getMethodIfString(Method m) {
        
        boolean onlyOneString = false;
        Class<?>[] params = m.getParameterTypes();
        
        for(Class p : params) {
            if(p.getCanonicalName().equals("java.lang.String")) {
                if(!onlyOneString) 
                    onlyOneString = true;
                
                else {
                    onlyOneString = false;
                    break;
                }
            }
        }
        
        return onlyOneString ? m : null;   
    }
}
