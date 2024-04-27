#import spCommons.spTimer as st
#from spCommons.spTimer import spTimer as st # st.ShowTime 
import spCommons.spTimer as st   # st.spTimer.ShowTime and st.directShowTime

#@st.showTime
@st.spTimer.ShowTime
def say_hello(): 
    print("Hello Geeks!") 

  
def say_bye(): 
    print("Bye Geeks!") 
say_bye = st.spTimer.ShowTime(say_bye)
 
say_hello() 
say_bye() 


class Person:		
	def __init__(self, name, age):	
		self.name = name
		self.age = age
	def __str__(self):	
		return f"{self.name} - ({self.age})"
	def myfunc(self, abc):	
		print("Hello my name is " + abc)


p = Person("Sujata",56)
p.myfunc("passed parm")