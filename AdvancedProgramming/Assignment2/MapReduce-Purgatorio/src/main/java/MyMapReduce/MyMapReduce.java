/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package MyMapReduce;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.stream.Stream;

/**
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 * @param <T1> The initial Key type to be read from the read() method
 * @param <T2> The initial Value type to be read from the read() method
 * @param <T3> The "unique" Key type, result of the map() method
 * @param <T4> The result Value type of the map() method
 * @param <T5> The final Value type that will be written
 */
public abstract class MyMapReduce<T1, T2, T3, T4, T5> {
    
    protected abstract Stream<Pair<T1, T2>> read();
    protected abstract Stream<Pair<T3, T4>> map(Stream<Pair<T1,T2>> s);
    protected abstract Stream<Pair<T3, T5>> reduce(Stream<Pair<T3, List<T4>>> s);
    protected abstract void write(Stream<Pair<T3, T5>> s);
    
    private Stream<Pair<T3, List<T4>>> groupByKey(Stream<Pair<T3, T4>> s) {
        
        Map<T3, List<T4>> tree = new TreeMap<>(this::compare);
        
        s.forEach(pair -> { 
            tree.computeIfAbsent(pair.getKey(), k -> new LinkedList<>()).add(pair.getValue());
        });
        /*
        
        s.forEach(pair -> {
            
            T3 keys = pair.getKey();
            T4 valueToAppend = pair.getValue();
            tree.merge(keys, new LinkedList<>(), (key, values) -> values).add(valueToAppend);

        });
        */
        System.out.println(tree.entrySet());
        //System.out.println(Arrays.toString(tree.get("able").toArray()));
        return tree.entrySet().stream().map(res -> new Pair(res.getKey(), res.getValue()));
    }
    
    protected abstract int compare(T3 k1, T3 k2);
    
    /**
     * Sequential implementation of the MapReduce framework. 
     * Since it's a sequential MapReduce framework, there's no need to
     * split the results of, let's say, map to give it to different
     * threads/machines. That's why the method simply calls these
     * methods in this order, without further ado.
     */
    public final void sequentialMapReduce() {
        write(reduce(groupByKey(map(read()))));
    }
}
