# part of https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/5/tagging-and-extraction
#working
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

'''
Doing it for real¶
=================
Tagging
--------
We can apply tagging to a larger body of text.
For example, let's load this blog post and extract tag information from a sub-set of the text.
'''
#deprecated from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
documents = loader.load()

doc = documents[0]

page_content = doc.page_content[:10000] #get first 10000 chars
# print(page_content[:1000]) #print first 1000 chars


from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

#Deprecated
from pydantic import BaseModel, Field    #Basemodel helps type checking
#from langchain_core.pydantic_v1 import BaseModel, Field  #DID NOT DETECT missing func desc
#from typing import List, Optional       #to make lists and optional field 

class Overview(BaseModel):
    """Overview of a section of text."""
    summary: str = Field(description="Provide a concise summary of the content.")
    language: str = Field(description="Provide the language that the content is written in.")
    keywords: str = Field(description="Provide keywords related to the content.")
    
#Deprectaed from langchain.utils.openai_functions import convert_pydantic_to_openai_function
#Deprectaed weather_function = convert_pydantic_to_openai_function(WeatherSearch)
#Decprecated from langchain_core.utils.function_calling import convert_pydantic_to_openai_function as fConv
from langchain_core.utils.function_calling import convert_to_openai_function as fConv
overview_tagging_function = [
    fConv(Overview)
]

#Deprecated from langchain.chat_models import ChatOpenAI
#Deprecated from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
model = ChatOpenAI(temperature=0)
tagging_model = model.bind(
    functions=overview_tagging_function,
    function_call={"name":"Overview"}  #forces function call.
)

#parsing 
# from langchain.schema.output_parser import StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
# from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
# from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

tagging_chain = prompt | tagging_model | JsonOutputFunctionsParser()

result=tagging_chain.invoke({"input": page_content})
import json
print(json.dumps(result))   #print the result

'''
Extraction
================
'''

from typing import List, Optional       #to make lists and optional field 
class Paper(BaseModel):
    """Information about papers mentioned."""
    title: str
    author: Optional[str]


class Info(BaseModel):
    """Information to extract"""
    papers: List[Paper]
    
#Deprectaed from langchain.utils.openai_functions import convert_pydantic_to_openai_function as fConv
#Decprecated BUT ONLY This worrks 
from langchain_core.utils.function_calling import convert_pydantic_to_openai_function as fConv
#Recommended but does not return any arguments for function calling 
#from langchain_core.utils.function_calling import convert_to_openai_function as fConv
paper_extraction_function = [
    fConv(Info)
]
extraction_model = model.bind(
    functions=paper_extraction_function, 
    function_call={"name":"Info"}
)

'''#Old template: but returns tehhis article an dauthor name. Not the mentioned ones.
prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract the relevant information, if not explicitly provided do not guess. Extract partial info"),
    ("human", "{input}")
])

'''
#modify prompt to return papers mentioned, along with authors
template = """A article will be passed to you. Extract from it all papers, along with their authors, that are mentioned by this article. 

Do not extract the name of the article itself. If no papers are mentioned that's fine - you don't need to extract any! Just return an empty list.

Do not make up or guess ANY extra information. Only extract what exactly is in the text."""

from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", "{input}")
])
#parsing 
# from langchain.schema.output_parser import StrOutputParser
# from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
# from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
extraction_chain = prompt | extraction_model | JsonKeyOutputFunctionsParser(key_name="papers")
result=extraction_chain.invoke({"input": page_content})
import json                   # pretty print json
for  r in result: print(json.dumps(r))   #print the result

extraction_chain.invoke({"input": "hi"})

#######FULL ARTICLE##################################### # article is really long. 
# Will be too big for the token windows. SO pass each chunk individually and combine teh results. 
# use runnable lambda to loop over chunks , pass it to our previous chain, and then flatten list of lists

# join/flatten list of lists
def flatten(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list
if __name__=="__main__":
    print(flatten([[1,2,3],['A',4,5]]))          

# split into chuncks
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_overlap=0)   
splits = text_splitter.split_text(doc.page_content)

print("count of splits:" + str(len(splits)))
#print(splits[0])
from langchain.schema.runnable import RunnableLambda
# prep teh model/chain input
# i.e for result=extraction_chain.invoke({"input": page_content})

prep = RunnableLambda(
    lambda x: [{"input": doc} for doc in text_splitter.split_text(x)]
)

prep.invoke("hi") #[{'input': 'hi'}]
chain = prep | extraction_chain.map() | flatten
result = chain.invoke(doc.page_content)
import json                   # pretty print json
for  r in result: print(json.dumps(r))   #print the result
len(result)