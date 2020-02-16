/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Exercise4;

import MyMapReduce.MyMapReduce;
import MyMapReduce.Pair;
import MyMapReduce.Reader;
import MyMapReduce.Writer;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.TreeMap;
import java.util.stream.Stream;

/**
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
public class CountingWords extends MyMapReduce<String, List<String>, String, Integer, Integer> {

    @Override
    protected Stream<Pair<String, List<String>>> read() {
        
        /* "The program should ask the user for the absolute path of the directory 
        where documents are stored. Only files ending in .txt should be considered." */
        System.out.println("Write the absolute path of the directory where documents are stored");
        Scanner s = new Scanner(System.in);
        String input = s.nextLine();
        
        Path p = Paths.get(input);
        
        /* The read function must return a stream of pairs (fileName, contents),
        where filename is the name of the text file and contents is a list of strings, 
        one for each line of the file. For the read function you can exploit the 
        enclosed class Reader.java in the way you prefer. */
        Reader r = new Reader(p);
        
        try {                  
            return r.read();
        } catch (IOException e) {
            System.err.println("Error during read() method: " + e.getMessage()); return null;
        }
    }

    
    /*  Must return a stream of pairs containing, for each word (of length 
        greater than 3) in a line, the pair (w, k) where k is the number 
        of occurrences of w in that line. */
    @Override
    protected Stream<Pair<String, Integer>> map(Stream<Pair<String, List<String>>> s) {
        
        Map<String, Integer> tree = new TreeMap<>(String::compareTo);
        
        s.forEach(pair -> { 
            List<String> lines = pair.getValue(); 
            lines.forEach((l) -> {
                
                String[] ws = l.split(" ");
                
                Arrays.stream(ws)
                        .filter(w -> w.length() > 3)
                        .map(w -> w.toLowerCase().replaceAll("[^a-z0-9]", ""))
                        .forEach(w -> tree.put(w, tree.getOrDefault(w, 0)+1));
                }
            );
        });
        
        return tree.entrySet().stream().map(res -> new Pair(res.getKey(), res.getValue()));
    }


    /**
     * The compare function should compare strings according to the standard alphanumeric ordering.
     * @param s1 The string to compare
     * @param s2 The string to be compared to
     * @return an integer, representing the comparison between the two strings
     */
    @Override
    protected int compare(String s1, String s2) {
        return s1.compareTo(s2);
    }

    @Override
    protected Stream<Pair<String, Integer>> reduce(Stream<Pair<String, List<Integer>>> s) {
        
        Map<String, Integer> tree = new TreeMap<>();
        
        s.forEach(pair -> {
            List<Integer> values = pair.getValue();
            Integer x = values.stream().map((v) -> v).reduce(0, Integer::sum);
            tree.put(pair.getKey(), x);
        });
        
        return tree.entrySet().stream().map(res -> new Pair(res.getKey(), res.getValue()));
    }

    @Override
    protected void write(Stream<Pair<String, Integer>> s) {
        File dst = new File("output.csv");
        try {
            Writer.write(dst, s);
        } catch (FileNotFoundException e) { System.err.println("Error during the write() method: " + e.getMessage()); return; }
    }
}