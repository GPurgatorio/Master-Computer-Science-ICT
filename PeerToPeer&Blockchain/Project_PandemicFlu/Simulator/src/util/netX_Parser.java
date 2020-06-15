package util;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

public class netX_Parser {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("reports/paste.txt"));
        String s;
        Map<String, LinkedList<Tuple<String, Integer>>> start = new HashMap<>();

        while((s = br.readLine()) != null) {
            if(s.startsWith("\"") || s.length() < 1 )
                continue;
            if(s.startsWith("First infected for")) {
                String[] split = s.split(" ");
                start.computeIfAbsent(split[5], k -> new LinkedList<>()).add(new Tuple(split[3], 1));
                continue;
            }

            String[] split = s.split(" ");
            start.computeIfAbsent(split[0], k -> new LinkedList<>()).add(new Tuple(split[2], split[4]));
        }

        Set<String> keys = start.keySet();
        for(String k : keys) {
            LinkedList<Tuple<String, Integer>> values = start.get(k);
            System.out.println(k + " infected a total of: " + values.size() + " hosts.\t");
            for(Tuple t : values) {
                System.out.println(t.getKey() + " at time " + t.getValue());
            }
            System.out.println("");
        }
    }
}
