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

## pretty print json with indent
import json
#print(get_current_temperature(24,24))
str="{'latitude': {'title': 'Latitude', 'description': 'Latitude of the location to fetch weather data for', 'type': 'number'}, 'longitude': {'title': 'Longitude', 'description': 'Longitude of the location to fetch weather data for', 'type': 'number'}}"
print(json.dumps(str, indent=4))    # indent parameter is neessary get pretty  indented print


#print on same line
print("result message log: ",end=" ")  # print on sameline Py3.x: use end="" print("geeks", end =" ") AND Py2.x:add a comma after print statement: print("xyz"),
