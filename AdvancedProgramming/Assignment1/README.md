# Exercise 1.1: Testing encryption functions

As you need to protect communications within your software company from hackers, you encharged an employee to implement a set of cryptographic algorithms. Each algorithm should be implemented by a Java class providing

A constructor taking an encryption key of type String as parameter
An encryption method taking a String as parameter and returning the encrypted string
A decryption method taking a String as parameter and returning the decrypted string
Unfortunately the employee decided to leave your company for a better job. Before leaving, he delivered to you the attached folder crypto containg the .class files only and some auxiliary files, claiming that his obligation was fulfilled. He told you that, at least for some of the algorithms, the encryption method starts with enc and the decryption method with dec, and that the encryption keys to be used were recorded in a file.

Clearly you don't trust completely the programmer anymore, thus you want to test his code. Do the following:

Define a KeyRegistry class, with methods:
- add (Class c, String key): to add a new key key for the crypto algorithm class c
- get (Class c): to get the last key of the type specified by c
Write a Java program TestAlgs that takes the parent directory of crypto as a command line argument (i.e., via argv) and:
- Loads the list of keys in the registry: each line in the file crypto/keys.list is a space-separated pair made of the class name of the algorithm and the key needed for such an algorithm
- For each class files in crypto/algos, first check if it is an encryption algorithm, i.e. it has (1) a public constructor, (2) a method starting with enc and (3) a method starting with dec, all three with one String parameter.
- If it is not an encryption algorithm just print a corresponding warning on the standard output.
- Otherwhise test the class as follows, using the secret words in file crypto/secret.list:
- For each secret word w (i.e., each line in file crypto/secret.list), create an instance of the algorithm using the correspoding key as argument to the constructor. Next call the encryption method on w, producing say e, and then the decryption method on e obtaining a string d. If d is different from w and it is not equal to w followed by one or more padding characters #, then print on the standard output, KO: w -> e -> d.

**Solution format:** The Java source files implementing the described algorithm, including at least KeyRegistry.java and the main class TestAlgs.java.


# Exercise 1.2: (Optional) Testing encryption functions, again, with annotations
Even if the testing program developed in Exercise 1.1 worked pretty well on some algorithms, some classes in crypto/algos were not identified as encryption algorithms. From a colleague of you former employee you learn that he liked very much to use annotations. Therefore, after inspecting folder crypto/annot, you suspect that also the remaining classes could implement an encryption algorithm: they use the annotations @Encrypt and @Decrypt to tag the encryption and the decryption method, respectively.

- Write a Java program TestAlgsPlus that enriches the testing framework of Exercise 1.1 in order to test also classes which contain (1) a public constructor, (2) exactly one method annotated with @Encrypt and (3) exactly one method annotated with @Decrypt, all three with one String parameter. If necessary, refactor the code of the previous exercise in order to reuse it as much as possible here.
- Rewrite the source code of the @Encrypt and @Decrypt annotations, making them visible at runtime

**Solution format:** The Java source files Encrypt.java and Decrypt.java defining the two annotations, and the Java source files implementing the algorithm, including at least TestAlgsPlus.java.



# Exercise 2: Drones
Since your company is now safe from hackers, you can spend your free time by flying your fleet of drones.

**Exercise 2a**
In a new NetBeans project called Drones-<yourSurname> define a Java bean Drone with a read-only property loc (that expresses the current position of the drone in a 2D grid), and a boolean property flying (telling whether the drone is flying or not). Also, provide the following two methods:

- takeOff(initLoc), that sets flying to true, initializes loc to initLoc, and sets up a Timer to generate a new location for the drone each second (with a displacement in each direction within -10 and +10)
- land(), that stops the timer, sets flying to false and leaves loc unchanged.
Drone must also provide methods for adding and removing listeners to PropertyChangeEvent. Such an event must be fired at each change of loc and flying.

**Exercise 2b**
In the same NetBeans project of the previous exercise, write a new Java GUI application, that includes a JPanel (call it pnlDrones) and a JButton (call it btnAdd).

Upon a click on btnAdd the application must:

- Create a new Drone (call it newDrone)
- Inside pnlDrones, create a new JLabel with a random foreground color:
- The label must subscribe as a PropertyChangeListener to newDrone (for that, extend JLabel as needed)
- It should move in pnlDrones to follow the position of newDrone. Note that in any case the JLabel must stay within the limits of pnlDrones
- Its text must be >x,y< if the drone is flying, and <x,y> otherwise, where x and y are the coordinates of the current location of the drone
- Upon click on the label, the land() method of the corresponding drone must be invoked

*Hint: to move the labels programmatically, choose the null layout for pnlDrones from the Navigator window in NetBeans and use the method setBounds of the label you want to move.*

**Solution format:** An archive Drones-<yourSurname>.zip containing the NetBeans project developed for Exercise 2a and Exercise 2b.