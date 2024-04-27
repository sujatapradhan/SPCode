def f1(p): print ("Called f1 with " + p)				
def f2(p):print ("Called f2 with " + p)				
ff=f1                   #Function aliasing				
ff("ff equated to f1 ")				
				
print(type(f1))				
def df(f, p): f(p)				
df(f1, "passed df with f1")				
df(f2, "passed df with f2")				
				
#
# calling func => DecFunc will be called first and then it wil call func			
				
				
				
def DecFunc(f):				
	def wrapper(*args , **kwargs):			
		print("\n============" )		
		print("do some Dec Func stuff first")		
		print("calling ___" + f.__name__)		
		val = f(*args , **kwargs)		
		print("do some Dec Func follow up stuff")		
		return val		
	return wrapper			
				
def f3(): print ("Called f3 no parm ")				
DecFunc(f3)()				
#OR				
f = DecFunc(f3)  #function aliasing				
f()				
				
#OR				
@DecFunc    #decoration   pre call aFunc with  f4 called inside aFunc				
def f4(): print ("Called f4 no parm ")				
f4()           # aFunc will becalled first and then it wil call f4				
				
@DecFunc    #decoration   pre call aFunc with  f4 called inside aFunc				
def f5( s, num): print ("Called f5 with parm " + s + " and " + str(num))				
f5("Some String", 123)           # aFunc will becalled first and then it wil call f5 with any number of parms				