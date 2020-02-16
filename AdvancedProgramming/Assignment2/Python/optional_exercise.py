import os
import requests


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
    do_exercise()
