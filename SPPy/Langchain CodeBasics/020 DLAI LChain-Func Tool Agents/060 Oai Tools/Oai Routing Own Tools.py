# https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/6/tools-and-routing
# working
print("Start-------------------------------------")
###### Set up Subdirectiry package importing 
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) #SO that subdir package import works
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

import json # to handle json stuff like json.dumps (jsonStr)

'''
Tool Usage
=================
Tools: Functions & services LLM can use to extend its capabilites:
    1) LLM must decide which function and what are teh inputs
    2) Calling it with thoose inputs
    
Tool does both - 
    a schema def for a func
    then conv into openai func spec
    a callable to call that model
many built in tool
    serach tool
    math tool
    sql tool
But here we build our own tool
    create
    hwo to use a llm to select which tool to use
    call thos etools
'''

### type checking using pydantic
from langchain.agents import tool 

#failed from pydantic import BaseModel, Field
# https://stackoverflow.com/questions/77679383/validationerror-1-validation-error-for-structuredtool
# used teh 2nd answer as it was easy and it worked
from pydantic.v1 import BaseModel, Field

import datetime
# Define the input schema
class OpenMeteoInput(BaseModel):
    latitude: float = Field(..., description="Latitude of the location to fetch weather data for")
    longitude: float = Field(..., description="Longitude of the location to fetch weather data for")

@tool(args_schema=OpenMeteoInput)
def get_current_temperature(latitude: float, longitude: float) -> dict:
    """Fetch current temperature for given coordinates."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    # Parameters for the request
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }

    import requests

    # Make the request
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()
    else:
        raise Exception(f"API Request failed with status code: {response.status_code}")
    #for time_str in results['hourly']['time']: print(time_str) 
     
    
    #deprecated # 
    current_utc_time = datetime.datetime.utcnow()
    #shoudl be # current_utc_time = datetime.datetime.now(datetime.UTC)
    time_list = [datetime.datetime.fromisoformat(time_str.replace('Z', '+00:00')) for time_str in results['hourly']['time']]
    temperature_list = results['hourly']['temperature_2m']
    
    #print(str(time_list[1]) + " - " + str(current_utc_time)) #for i in range(len(time_list))
    #2024-04-30 01:00:00 - 2024-04-30 18:09:42.107778+00:00
    
    #from spCommons import spTimer as st   # st.spTimer.ShowTime and st.directShowTime
    #closest_time_index = min(range(len(time_list)), key=lambda i: abs(st.spTimer.spNaiveToUTC(time_list[i],datetime.UTC) - current_utc_time))
    closest_time_index = min(range(len(time_list)), key=lambda i: abs(time_list[i] - current_utc_time))
    current_temperature = temperature_list[closest_time_index]
    #current_temperature=99
    return f'The current temperature is {current_temperature}°C'
    
import json
# now you have extra propoerties
#print(get_current_temperature.name)
#print(get_current_temperature.description)
#print(json.dumps(get_current_temperature.args, indent=4))    # indent parameter is neessary get pretty  indented print

#map to openai
#deprecated # from langchain.tools.render import format_tool_to_openai_function
#failed # print(json.dumps(format_tool_to_openai_function(get_current_temperature),indent=4))
from langchain_core.utils.function_calling import convert_to_openai_function
#print(json.dumps(
convert_to_openai_function(get_current_temperature)
#,indent=4))

#print(get_current_temperature(24,24)) # direct fparameter passing wont wwork. Needs json format
print(get_current_temperature({"latitude": 24, "longitude": 24}))



import wikipedia
@tool
def search_wikipedia(query: str) -> str:
    """Run Wikipedia search and get page summaries."""
    page_titles = wikipedia.search(query)
    summaries = []
    for page_title in page_titles[: 3]:
        try:
            wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
            summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
        except (
            self.wiki_client.exceptions.PageError,
            self.wiki_client.exceptions.DisambiguationError,
        ):
            pass
    if not summaries:
        return "No good Wikipedia Search Result was found"
    return "\n\n".join(summaries)

import json
# now you have extra propoerties
#print(search_wikipedia.name)
#print(search_wikipedia.description)
#print(json.dumps(search_wikipedia.args, indent=4))    # indent parameter is neessary get pretty  indented print
#print(json.dumps(
convert_to_openai_function(search_wikipedia)
#,indent=4))

##########print(search_wikipedia({"query": "langchain"}))


#map to openai
#deprecated # 
from langchain.tools.render import format_tool_to_openai_function
#failed # print(json.dumps(format_tool_to_openai_function(get_current_temperature),indent=4))
from langchain_core.utils.function_calling import convert_to_openai_function
print(json.dumps(convert_to_openai_function(get_current_temperature),indent=4))

functions = [
    format_tool_to_openai_function(f) for f in [
        search_wikipedia, get_current_temperature
    ]
]
from langchain.chat_models import ChatOpenAI
model = ChatOpenAI(temperature=0).bind(functions=functions)

print("what is the weather in sf right now")
print(model.invoke("what is the weather in sf right now").additional_kwargs)
print("what is langchain")
print(model.invoke("what is langchain").additional_kwargs)


from langchain.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    ("user", "{input}"),
])
chain = prompt | model
print(chain.invoke({"input": "what is the weather in sf right now"}))

from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
chain = prompt | model | OpenAIFunctionsAgentOutputParser()
result = chain.invoke({"input": "what is the weather in sf right now"})
print(type(result))
print(result.tool)
print(result.tool_input )
print(get_current_temperature(result.tool_input))

result = chain.invoke({"input": "hi!"})
print(type(result))
print(result.return_values)

from langchain.schema.agent import AgentFinish
def route(result):
    if isinstance(result, AgentFinish):
        return result.return_values['output']
    else:
        tools = {
            "search_wikipedia": search_wikipedia, 
            "get_current_temperature": get_current_temperature,
        }
        return tools[result.tool].run(result.tool_input)
chain = prompt | model | OpenAIFunctionsAgentOutputParser() | route
result = chain.invoke({"input": "What is the weather in san francisco right now?"})
print(result)
result = chain.invoke({"input": "What is langchain?"})
print(result)
result = chain.invoke({"input": "hi!"})
print(result)
