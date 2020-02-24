import time
import csv
import threading
from statistics import stdev, mean, pstdev
# for the optional exercise only
import os
import requests

# Mandatory Exercise (Benchmark)

# the number of runs the script should execute before the actual iterations
WARMUPS = 5
# the number of runs the script should execute and count towards final statistics
ITER = 3
# adds prints
VERBOSE = True

""" 
    "When invoking a function fun decorated by benchmark, fun is executed possibly 
    several times (discarding the results) and a small table is printed on the standard 
    output including the average time of execution and the variance."
"""


def benchmark(warmups=0, iter=1, verbose=False, csv_file=None):
    def decorator(method):

        def timed(*args, **kwargs):

            f = None
            times = []

            if csv_file:
                f = open(csv_file + ".csv", mode="w")
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(["run num", "is warmup", "timing"])

            if verbose:
                print("Run #\t|\tType\t|\tTime")

            for i in range(warmups):
                ts = time.time()
                method(*args, **kwargs)
                te = time.time() - ts
                if verbose:
                    print('%d\t|\twarmup\t|\t%2.2f ms' % (i + 1, te * 1000))
                if f:
                    csv_writer.writerow([str(i + 1), "True", "N/D"])

            for i in range(iter):
                ts = time.time()
                method(*args, **kwargs)
                te = time.time() - ts
                times.append(te)
                if verbose:
                    print('%d\t|\titer\t|\t%2.2f ms' % (i + 1, te * 1000))
                if f:
                    csv_writer.writerow([str(i + 1), "False", str(int((te * 100000)) / 100)])

            if f:
                f.close()

            if verbose:
                print("\nAverage Time Requested: " + str(mean(times) * 1000) + " ms")
                print("(Sample) Standard Deviation: " + str(stdev(times) * 1000) + " ms")
                print("(Population) Standard Deviation: " + str(pstdev(times) * 1000) + " ms")

            print("Benchmark ended for %r" % method.__name__)

        return timed

    return decorator


# Test Fibonacci

def auxiliary_foo(f, *args, **kwargs):
    def test_settings(nthreads, ntimes):

        @benchmark(warmups=WARMUPS, iter=ITER, verbose=VERBOSE, csv_file="f_" + str(nthreads) + "_" + str(ntimes))
        def wrapper():

            # Repeat n times the function f with the arguments that are being passed
            def repeat_n(n):
                for _ in range(n):
                    # print this to see the result of Fibonacci
                    f(*args, **kwargs)

            pool = []

            # Create n threads
            for _ in range(nthreads):
                pool.append(threading.Thread(target=repeat_n, args=(ntimes,), kwargs=kwargs))

            # Start (and join) them
            for t in pool:
                t.start()
            for t in pool:
                t.join()

        return wrapper

    print("\n1 Threads, 16 Repetitions")
    test_settings(1, 16)()

    print("\n2 Threads, 8 Repetitions")
    test_settings(2, 8)()

    print("\n4 Threads, 4 Repetitions")
    test_settings(4, 4)()

    print("\n8 Threads, 2 Repetitions")
    test_settings(8, 2)()


# "Computes the n-th Fibonacci number in the standard, inefficient, double recursive way"
def fibonacci(n):
    if n > 2:
        return fibonacci(n - 1) + fibonacci(n - 2)
    else:
        return 1


# Optional Exercise

PRE_URL = "http://pages.di.unipi.it/corradini/Didattica/AP-19/PROG-ASS/02/pre.py"
POST_URL = "http://pages.di.unipi.it/corradini/Didattica/AP-19/PROG-ASS/02/post.py"
PRE_FILE = "pre_file.py"
POST_FILE = "post_file.py"

""" 
    Define another decorator called prepost taking as parameters two URLs, 
    the first indicating the location of a Python script to be executed before 
    the function being decorated, the second denoting the location of a 
    Python script to be executed after the function being decorated.
"""


def prepost(pre_function, post_function):
    # GET request to get the files
    x = requests.get(pre_function)
    y = requests.get(post_function)

    # writing what I received into a file
    pre_file = open(PRE_FILE, mode="w")
    post_file = open(POST_FILE, mode="w")
    pre_file.write(x.text)
    post_file.write(y.text)

    def decorator(method):
        def wrapper(*args, **kwargs):
            # Invoke the Python interpreter for the first script
            os.system("python3 " + PRE_FILE)
            # Do the middle operation
            method(*args, **kwargs)
            # Invoke the Python interpreter for the second script
            os.system("python3 " + POST_FILE)

        return wrapper

    return decorator


# Simple middle operation between the two scripts
@prepost(PRE_URL, POST_URL)
def do_exercise():
    print("This is an optional exercise :)")


if __name__ == "__main__":
    print("Fibonacci")
    auxiliary_foo(fibonacci, 25)

    # Note: requires an internet connection!
    print("\nOptional Exercise")
    do_exercise()

"""

As we can see by simply running this file, the time requested to execute the threads isn't better 
when increasing the number of threads, which would seem weird in the most of today's languages,
but not in Python because of the GIL (Global Interpreter Lock) which implies that only one
thread can be executed at a time, even if we try to force multi-thread like we did here.

Note: the first run (which is 1 thread 16 reps) has the best results. Having one single thread
doing the same work that many threads would do, due to lock delays, is (slightly) faster than
the multi-threaded version! 


Results:

1 Threads, 16 Repetitions
Run #	|	Type	|	Time
1	|	warmup	|	303.37 ms
2	|	warmup	|	290.90 ms
3	|	warmup	|	296.00 ms
4	|	warmup	|	290.77 ms
5	|	warmup	|	288.31 ms
1	|	iter	|	289.64 ms
2	|	iter	|	288.31 ms
3	|	iter	|	285.06 ms

Average Time Requested: 287.6693407694499 ms
(Sample) Standard Deviation: 2.357681648227026 ms
(Population) Standard Deviation: 1.925039004693413 ms
Benchmark ended for 'wrapper'

2 Threads, 8 Repetitions
Run #	|	Type	|	Time
1	|	warmup	|	422.30 ms
2	|	warmup	|	437.94 ms
3	|	warmup	|	415.76 ms
4	|	warmup	|	441.77 ms
5	|	warmup	|	447.85 ms
1	|	iter	|	452.57 ms
2	|	iter	|	440.11 ms
3	|	iter	|	445.29 ms

Average Time Requested: 445.99080085754395 ms
(Sample) Standard Deviation: 6.258410212627445 ms
(Population) Standard Deviation: 5.109970540653472 ms
Benchmark ended for 'wrapper'

4 Threads, 4 Repetitions
Run #	|	Type	|	Time
1	|	warmup	|	401.29 ms
2	|	warmup	|	438.29 ms
3	|	warmup	|	430.22 ms
4	|	warmup	|	446.11 ms
5	|	warmup	|	428.94 ms
1	|	iter	|	426.18 ms
2	|	iter	|	406.56 ms
3	|	iter	|	415.74 ms

Average Time Requested: 416.16185506184894 ms
(Sample) Standard Deviation: 9.814661481000755 ms
(Population) Standard Deviation: 8.013637542200168 ms
Benchmark ended for 'wrapper'

8 Threads, 2 Repetitions
Run #	|	Type	|	Time
1	|	warmup	|	420.40 ms
2	|	warmup	|	392.44 ms
3	|	warmup	|	412.61 ms
4	|	warmup	|	432.99 ms
5	|	warmup	|	394.43 ms
1	|	iter	|	419.54 ms
2	|	iter	|	419.36 ms
3	|	iter	|	419.07 ms

Average Time Requested: 419.3197886149089 ms
(Sample) Standard Deviation: 0.23714827841028413 ms
(Population) Standard Deviation: 0.19363075849489345 ms
Benchmark ended for 'wrapper'

"""
