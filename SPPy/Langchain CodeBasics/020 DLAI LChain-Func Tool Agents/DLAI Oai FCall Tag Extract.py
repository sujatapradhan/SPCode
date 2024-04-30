# https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/6/tools-and-routing
print("Start-------------------------------------")
###### Set up Subdirectiry package importing 
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works
#from spCommons.spTimer import spTimer as st # st.ShowTime 
##import spCommons.spTimer as st   # st.spTimer.ShowTime and st.directShowTime

########Set up env variables in main##############################
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
#load_dotenv(../.env) # if outside project folder
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]
#print("Hello ",os.environ["HUGGINGFACEHUB_API_TOKEN"])
#OR in google colab add Key as secret. GROQ_API_KEY. 
# from google.colab import userdata # and access it as userdata.get('GROQ_API_KEY')

from langchain.agents import tool


import langchain_core.utils
import langchain_core.utils.function_calling

from langchain.prompts import ChatPromptTemplate
#deprecated from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

from typing import List
#Deprecated
from pydantic import BaseModel, Field    #Basemodel helps type checking
#from langchain_core.pydantic_v1 import BaseModel, Field  #DID NOT DETECT missing func desc
    
#Deprectaed from langchain.utils.openai_functions import convert_pydantic_to_openai_function
#Deprectaed weather_function = convert_pydantic_to_openai_function(WeatherSearch)
import langchain_core  # part of some thing?
#weather_function=langchain_core.utils.function_calling.convert_to_openai_function(WeatherSearch)

import json                   # pretty print json
from langchain_openai import ChatOpenAI


'''
Tagging and Extraction Using OpenAI functions
================================================
Tagging
--------
'''

from typing import List
from pydantic import BaseModel, Field
from langchain.utils.openai_functions import convert_pydantic_to_openai_function


class Tagging(BaseModel):
    """Tag the piece of text with particular info."""
    sentiment: str = Field(description="sentiment of text, should be `pos`, `neg`, or `neutral`")
    language: str = Field(description="language of text (should be ISO 639-1 code)")
    
convert_pydantic_to_openai_function(Tagging)

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI


model = ChatOpenAI(temperature=0)

tagging_functions = [convert_pydantic_to_openai_function(Tagging)]


prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

model_with_functions = model.bind(
    functions=tagging_functions,
    function_call={"name": "Tagging"}
)

tagging_chain = prompt | model_with_functions

tagging_chain.invoke({"input": "I love langchain"})


tagging_chain.invoke({"input": "non mi piace questo cibo"})


from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

tagging_chain = prompt | model_with_functions | JsonOutputFunctionsParser()

tagging_chain.invoke({"input": "non mi piace questo cibo"})

'''
Extraction
---------
Extraction is similar to tagging, but used for extracting multiple pieces of information.
'''

from typing import Optional
class Person(BaseModel):
    """Information about a person."""
    name: str = Field(description="person's name")
    age: Optional[int] = Field(description="person's age")
class Information(BaseModel):
    """Information to extract."""
    people: List[Person] = Field(description="List of info about people")
convert_pydantic_to_openai_function(Information)

extraction_functions = [convert_pydantic_to_openai_function(Information)]
extraction_model = model.bind(functions=extraction_functions, function_call={"name": "Information"})

extraction_model.invoke("Joe is 30, his mom is Martha")



prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info. DO not include the attribute at all."),
    ("human", "{input}")
])

extraction_chain = prompt | extraction_model
extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"})

extraction_chain = prompt | extraction_model | JsonOutputFunctionsParser()
extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"})

from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="people")
extraction_chain.invoke({"input": "Joe is 30, his mom is Martha"}) # unexpectedly Still including age attribute as NOne
'''
Doing it for real
===============================
We can apply tagging to a larger body of text.

For example, let's load this blog post and extract tag information 
from a sub-set of the text.
'''

from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
documents = loader.load()

doc = documents[0]

page_content = doc.page_content[:10000] #get first 10000 chars
print(page_content[:1000]) #print first 1000 chars


prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")
    
overview_tagging_function = [
    convert_pydantic_to_openai_function(Overview)
]
tagging_model = model.bind(
    functions=overview_tagging_function,
    function_call={"name":"Overview"}
)
tagging_chain = prompt | tagging_model | JsonOutputFunctionsParser()

tagging_chain.invoke({"input": page_content})

