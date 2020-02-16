package TestAlgs;

public class Pair<T1,T2>{
    
    T1 first;
    T2 second;
    
    public Pair(T1 key , T2 value){
	this.first = key;
	this.second = value;
    }
    
    public T1 getKey(){
	return first;
    }

    public T2 getValue(){
	return second;
    }
    
    public String toString(){
        return "First: " + first + "\nSecond: " + second;
    }
    
    public boolean bothNotNull() {
        return null != first && null != second;
    }
}

