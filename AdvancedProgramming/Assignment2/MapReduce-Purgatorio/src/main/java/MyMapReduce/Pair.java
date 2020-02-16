package MyMapReduce;

public class Pair<T1,T2>{
    
    T1 key;
    T2 value;
    
    public Pair(T1 key , T2 value){
	this.key = key;
	this.value = value;
    }
    
    public T1 getKey(){
	return key;
    }

    public T2 getValue(){
	return value;
    }
    
    public String toString(){
        return "Key: " + key + "\nValue: " + value;
    }
}

