class spTimer:
    def ShowTime(func): 
        def wrapper_function(*args, **kwargs): #to help variable parameter passing
            import time
            start = time.time()
            func(*args,  **kwargs) 
            end = time.time()
            print("The time of execution of ",func.__name__," is :",(end-start) * 10**3, "ms")
        return wrapper_function 




def directShowTime(func): 
    def wrapper_function(*args, **kwargs):  #to help variable parameter passing
      import time
      start = time.time()
      func(*args,  **kwargs) 
      end = time.time()
      print("The time of execution of ",func.__name__," is :",(end-start) * 10**3, "ms")
    return wrapper_function 
  
  
@spTimer.ShowTime
def say_hello(): 
    print("Hello Geeks!") 
  
def say_bye(): 
    print("Bye Geeks!") 
say_bye = spTimer.ShowTime(say_bye)
 
if __name__ == "__main__":
    print("Directly called")
    say_hello() 
    say_bye() 
else:
    pass

