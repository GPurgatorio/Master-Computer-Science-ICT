package util;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;

public class graphParser {

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader("reports/paste2.txt"));
        String s, res = "";
        Map<String, LinkedList<Tuple<String, Integer>>> start = new HashMap<>();

        while ((s = br.readLine()) != null) {
            if (s.length() < 1)
                continue;

            String[] split = s.split(" ");
            //start.computeIfAbsent(split[0], k -> new LinkedList<>()).add(new Tuple(split[2], split[4]));
            //System.out.println(split[0] + "\t\t" + split[2].substring(split[2].indexOf(':')+1) + "\t\t" +
                    //split[3].substring(split[3].indexOf(':')+1) + "\t\t" + split[4].substring(split[4].indexOf(':')+1));
            int v = 1;
            res = res + (Integer.parseInt(split[v].substring(split[v].indexOf(':')+1))/140) + ",";
        }
        System.out.println(res);
    }
}
