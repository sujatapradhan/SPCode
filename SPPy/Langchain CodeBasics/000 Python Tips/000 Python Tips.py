#####Reflection
import inspect

def spFuncName():
    # Get the stack of frames
    stack = inspect.stack()
    # The calling function is at index 1 (index 0 is the current function)
    return stack[1].function
    
def my_function():
    print(spFuncName())

def testReflection():
    print("\n"+spFuncName())
    my_function()

testReflection()

######Decorators#######################
### Fuctions can be returned
class spComm:
    def dec(func): 
        def wrapper(*args, **kwargs): #to help variable parameter passing
            print("start ",  spFuncName())
            func(*args,  **kwargs) 
            print("end ", spFuncName())
        return wrapper
@spComm.dec
def testDecorater(): 
    print("start ", spFuncName()) 
    print("end ", spFuncName()) 
#Test Dec
testDecorater()
    
#######################
import json
bStr=b"test"
str=bStr.decode()  # decode: Convert bytes/streamed strings to a string - can also specify  encoding: srtObj = byteObj.decode('utf-8')
print(type(str), str)


