# part of https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/5/tagging-and-extraction
#deprecated from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
documents = loader.load()

doc = documents[0]

page_content = doc.page_content[:10000] #get first 10000 chars
print(page_content[:1000]) #print first 1000 chars


from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "Think carefully, and then tag the text as instructed"),
    ("user", "{input}")
])

#Deprecated
from pydantic import BaseModel, Field    #Basemodel helps type checking
#from langchain_core.pydantic_v1 import BaseModel, Field  #DID NOT DETECT missing func desc

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

tagging_chain = prompt | tagging_model | JsonOutputFunctionsParser()

x=tagging_chain.invoke({"input": page_content})
print(x)
