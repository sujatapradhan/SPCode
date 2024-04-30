#https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/4/openai-function-calling-in-langchain
print("Start-------------------------------------")
###### Set up Subdirectiry package importing 
import os,sys

import langchain_core.utils
import langchain_core.utils.function_calling
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works
from spCommons.spTimer import spTimer as st # st.ShowTime 
#import spCommons.spTimer as st   # st.spTimer.ShowTime and st.directShowTime

########Set up env variables in main##############################
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
#load_dotenv(../.env) # if outside project folder
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]
#print("Hello ",os.environ["HUGGINGFACEHUB_API_TOKEN"])
#OR in google colab add Key as secret. GROQ_API_KEY. 
# from google.colab import userdata # and access it as userdata.get('GROQ_API_KEY')


from langchain.prompts import ChatPromptTemplate
#deprecated from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from typing import List
#Deprecated
from pydantic import BaseModel, Field    #Basemodel helps type checking
#from langchain_core.pydantic_v1 import BaseModel, Field  #DID NOT DETECT missing func desc
'''
Pydantic Syntax
==============
Pydantic data classes are a blend of Python's data classes with the validation power of Pydantic.
They offer a concise way to define data structures while ensuring that the data adheres to specified types and constraints.
In standard python you would create a class like this:
'''
class User:
    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email
foo = User(name="Joe",age=32, email="joe@gmail.com")
print(foo.name)

foo = User(name="Joe",age="bar", email="joe@gmail.com")
print(foo.age)



class pUser(BaseModel):
    name: str= Field(description="Full name of user")
    age: int
    email: str
foo_p = pUser(name="Jane", age=32, email="jane@gmail.com")
print(foo_p.name)

#fails
#foo_p = pUser(name="Joe",age="bar", email="joe@gmail.com")
#print(foo_p.age)

class Class(BaseModel):
    students: List[pUser]
obj = Class(
    students=[pUser(name="Jane", age=32, email="jane@gmail.com"),
              pUser(name="John", age=32, email="john@gmail.com")
              ]
)
print(obj)

'''
Pydantic to OpenAI function definition
'''

class WeatherSearch(BaseModel):
    '''Call this with an airport code to get the weather at that airport'''
    airport_code: str = Field(description="airport code to get weather for")
    
#Deprectaed from langchain.utils.openai_functions import convert_pydantic_to_openai_function
#Deprectaed weather_function = convert_pydantic_to_openai_function(WeatherSearch)
import langchain_core  # part of some thing?
weather_function=langchain_core.utils.function_calling.convert_to_openai_function(WeatherSearch)
print(WeatherSearch)
import json                   # pretty print json
print(json.dumps(weather_function, indent=4))    # can be used for function calling

#not passing doc string - required. shoudl fail. fails but weirdly by generating some weird
class WeatherSearch1(BaseModel):
    airport_code: str = Field(description="airport code to get weather for")
weather_function1=langchain_core.utils.function_calling.convert_to_openai_function(WeatherSearch1)
print(json.dumps(weather_function1, indent=4))    # can be used for function calling


#---------- di dnot detect misisng func desc properly

#deprecated from langchain.chat_models import ChatOpenAI
#deprecated from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

model = ChatOpenAI()
model.invoke("what is the weather in SF today?", functions=[weather_function])

