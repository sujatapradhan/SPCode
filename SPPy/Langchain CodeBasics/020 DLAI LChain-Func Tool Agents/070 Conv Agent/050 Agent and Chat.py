# https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/7/conversational-agent
# working fro agent, Panel is a little tricky
# Could not get a child class of langchain_openai.ChatOpenAI  to bind functions  

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


COnv Agents=Tool uage+CHat Memory+Agents
========================================
Agents:
    Agents are : LLM +code
    LLM reasons wat steps t take and calls for actions
Agent Loop
    Chooses a tool to use
    Observe steh output of teh tool
    repeats until stopping criteria:
        LLM determined (agent finsih???)
        Hard coded rules (max iteration)
SO we will
    1) build tools
    2) LCEL agnet loop
    3) Utilize agent_executer:
        implemnets agent loop
        add err handling, early stopping, tracing etc
        
'''


print("Start-------------------------------------")
###### Set up Subdirectiry package importing 
import os,sys
#chnage teh repetition of os.path.dirname( depending on the indentation of your calling file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) #SO that subdir package import works
from spCommons.spTimer import spTimer as st # st.ShowTime 
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
##############################################################################


##1) Define tools
############################################################################

### type checking using pydantic
from langchain.agents import tool 

#failed from pydantic import BaseModel, Field
# https://stackoverflow.com/questions/77679383/validationerror-1-validation-error-for-structuredtool
# used teh 2nd answer as it was easy and it worked
from pydantic.v1 import BaseModel, Field

import datetime

@tool
def create_your_own(query: str) -> str:
    """This function can do whatever you would like once you fill it in """
    print(type(query))
    return query[::-1]

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
#from langchain_core.utils.function_calling import convert_to_openai_function
##print(json.dumps(
#convert_to_openai_function(get_current_temperature)
##,indent=4))
##print(get_current_temperature(24,24)) # direct fparameter passing wont wwork. Needs json format
#print(get_current_temperature({"latitude": 24, "longitude": 24}))



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

##print(json.dumps(
#convert_to_openai_function(search_wikipedia)
##,indent=4))
#print(search_wikipedia({"query": "langchain"}))


##2========map to openai
############################################################################

#deprecated # from langchain.tools.render import format_tool_to_openai_function
#failed # print(json.dumps(format_tool_to_openai_function(get_current_temperature),indent=4))
from langchain_core.utils.function_calling import convert_to_openai_function
###print(json.dumps(convert_to_openai_function(get_current_temperature),indent=4))
##deleting as List
# tools = [search_wikipedia, get_current_temperature]
#functions = [convert_to_openai_function(f) for f in tools]

toolsDict = {   "search_wikipedia": search_wikipedia, 
                "get_current_temperature": get_current_temperature}
tools = [ f for fname, f in toolsDict.items()]
# you do notr require dict with gent Executer 
tools = [get_current_temperature, search_wikipedia, create_your_own]





##3========convert to functions and bind tools to model with temperature
############################################################################

#DeprecationWarning #from langchain.chat_models import ChatOpenAI 
#DeprecationWarning #from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
functions = [convert_to_openai_function(f) for fname,f in toolsDict.items()]
model = ChatOpenAI(temperature=0).bind(functions=functions)
'''
#Could not get a child class of langchain_openai.ChatOpenAI  to bind functions  
#DeprecationWarning #from langchain.chat_models import ChatOpenAI 
#DeprecationWarning #from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI #as ParentChatOpenAI
class TooledChatOpenAI (ChatOpenAI):   #Tooled ChatOpenAI
    toolsDict= {}
    def __init__(self, temperature, toolsDict):
        #self.toolsDict  = toolsDict
        functions = [convert_to_openai_function(f) for fname,f in toolsDict.items()]
        super().__init__(temperature=temperature)
        self.bind(functions=functions)
model = TooledChatOpenAI(temperature=0,toolsDict=toolsDict)
#model.bind(functions=functions)
'''



'''
### test
q="what is the weather in sf right now"
print(q)
print(model.invoke(q).additional_kwargs)
q="what is langchain"
print(q)
print(model.invoke(q).additional_kwargs)
q="Hi"
print(q)
print(model.invoke(q).additional_kwargs)
'''

##4========Create prompt with chat History
############################################################################

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")    # add extra MessagesPlaceholder line for  Tool call history to pass list of messages
])
#To do Chat so that previous con is remebred add a chat memeory
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    MessagesPlaceholder(variable_name="chat_history"),      # add for chat History and ensure has it in Runnable pass through
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")    # add extra MessagesPlaceholder line for  Tool call history to pass list of messages
])


'''#test
#chain = prompt | model
#print(chain.invoke({"input": "what is the weather in sf right now"}))
'''

##5========Create chain to invoke
############################################################################

from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
chain = prompt | model | OpenAIFunctionsAgentOutputParser()

##################################################################################################################################
##6========invoke chain manually creating every thing step by step OR switch to ##6 below
############################################################################

q= "what is the weather in sf right now"
'''
result = chain.invoke({"input": q,                            # returns AgentActionMessageLog   
                       "agent_scratchpad":[]                  # add extra line for chatmemory
                       })

#test
print(q + "-------------->")
print("result type: " + str(type(result)))
print("result tool: " + result.tool)
print("result tool inputs: " + str(result.tool_input) )
print("result message log: ",end=" ")  # print on sameline Py3.x: use end="" print("geeks", end =" ") AND Py2.x:add a comma after print statement: print("xyz"),
print(result.message_log )
print("result message log[0].additional_kwargs: ",end=" ")  # print on sameline Py3.x: use end="" print("geeks", end =" ") AND Py2.x:add a comma after print statement: print("xyz"),
print(json.dumps(result.message_log[0].additional_kwargs, indent=3) )
'''


##same as #observation = get_current_temperature(result.tool_input)
#observation = toolsDict[result.tool].run(result.tool_input)
##print("****"+observation)

#from langchain.agents.format_scratchpad import format_to_openai_functions
## Take the 2 things like resu;t of type AgentActionMessageLog and observation 
## and pass them back
#test=format_to_openai_functions([(result, observation), ])  #LIST OF TUPELES of func call and result
'''
#test
print(json.dumps(test[0].additional_kwargs, indent=3))
print(json.dumps(test[0].response_metadata, indent=3))
print(test)
print(test[0])   # [1] is func call
print(test[1])   # [1] is result of func call

#call it again  . 
# and since thsi is alreday has teh answer = it returns AgnetFinish with output and log
#AgentFinish(return_values={'output': 'The current temperature in San Francisco is 14.0°C.'}, log='The current temperature in San Francisco is 14.0°C.')
result2 = chain.invoke({
    "input": q, 
    "agent_scratchpad": format_to_openai_functions([(result, observation)])
})
result
result2

'''




'''
#The belwo if for understanding YOu can skip to AgnetExecutor directly

#So LOOP until AgentFinish
# thsi version not needed to be used
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.schema.agent import AgentFinish
def run_agent_V1(user_input):
    intermediate_steps = []
    while True:
        result = chain.invoke({
            "input": user_input, 
            "agent_scratchpad": format_to_openai_functions(intermediate_steps)
        })
        if isinstance(result, AgentFinish):
            return result
        toolsDict = {   "search_wikipedia": search_wikipedia, 
                        "get_current_temperature": get_current_temperature  }
        observation = toolsDict[result.tool].run(result.tool_input)
        intermediate_steps.append((result, observation))
# to make it cleaner move the  teh scartchpad format_to_openai_functions into teh chain agent
# so make it a runnable passthrough which takes the initial input and passes it trhough
#  SO assign of Runnable passthrough creates the parameter to be passed to chain
from langchain.schema.runnable import RunnablePassthrough
agent_chain = RunnablePassthrough.assign(                                               # assign creates a variable                
    agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
) | chain


#So LOOP until AgentFinish
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.schema.agent import AgentFinish
# thebelow is teh simple implemnetaion of AGentExecuter - beter loggoing, error handling for json and tools 
def run_agent(user_input, toolsDict):
    intermediate_steps = []
    while True:
        result = agent_chain.invoke({
            "input": user_input, 
            "intermediate_steps": intermediate_steps
        })
        if isinstance(result, AgentFinish):
            return result
        observation = toolsDict[result.tool].run(result.tool_input)
        intermediate_steps.append((result, observation))
        

output=run_agent("what is the weather in sf?",toolsDict)
print("**********************************************************************")
print(output)

output=run_agent("what is langchain?",toolsDict)
print("**********************************************************************")
print(output)

output=run_agent("hi!",toolsDict)
print("**********************************************************************")
print(output)
'''
##################################################################################################################################













##6========invoke chain  using AgentExecuter
# first do a pass through as we have added
# # to make it cleaner move the  teh scartchpad format_to_openai_functions into teh chain agent
# so make it a runnable passthrough which takes the initial input and passes it trhough
#  SO assign of Runnable passthrough creates the parameter to be passed to chain
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
## Take the 2 things like resu;t of type AgentActionMessageLog and observation 
## and pass them back
#Agent_chain to create, loop and pass through te intermediate steps so taht it knows what happened
agent_chain = RunnablePassthrough.assign(
    agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
) | prompt | model | OpenAIFunctionsAgentOutputParser()
### memory object for chat history to return in message format(return_messages=True), NOt string
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")


############################################################################
from langchain.agents import AgentExecutor
#agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True)
#with chat hostory or memory it wil not remeber
agent_executor = AgentExecutor(agent=agent_chain, tools=tools, verbose=True, memory=memory)


'''
#test
output = agent_executor.invoke({"input": "what is the weather in sf?"})
print("**********************************************************************")
print(output)

output = agent_executor.invoke({"input": "what is langchain?"})
print("**********************************************************************")
print(output)

output = agent_executor.invoke({"input": "hi!"})
print("**********************************************************************")
print(output)

output=agent_executor.invoke({"input": "my name is bob"})
print("**********************************************************************")
print(output)

output=agent_executor.invoke({"input": "What is my name?"})
#Now it  does remember
print("**********************************************************************")
print(output)


'''









###########################################################################################
# Create a chatbot
###########################################################################################
import panel as pn  # GUI
pn.extension()
import panel as pn
import param

class cbfs(param.Parameterized):
    
    def __init__(self, tools, **params):
        super(cbfs, self).__init__( **params)
        self.panels = []
        
        #map to openai
        #deprecated # from langchain.tools.render import format_tool_to_openai_function
        #failed # print(json.dumps(format_tool_to_openai_function(get_current_temperature),indent=4))
        #from langchain_core.utils.function_calling import convert_to_openai_function
        from langchain_core.utils.function_calling import convert_to_openai_function
        self.functions = [convert_to_openai_function(f) for f in tools]
        self.model = ChatOpenAI(temperature=0).bind(functions=self.functions)
        self.memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are helpful but sassy assistant"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        self.chain = RunnablePassthrough.assign(
            agent_scratchpad = lambda x: format_to_openai_functions(x["intermediate_steps"])
        ) | self.prompt | self.model | OpenAIFunctionsAgentOutputParser()
        self.qa = AgentExecutor(agent=self.chain, tools=tools, verbose=False, memory=self.memory)
    
    def convchain(self, query):
        if not query:
            return
        inp.value = ''
        result = self.qa.invoke({"input": query})
        self.answer = result['output'] 
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=450)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer, width=450, styles={'background-color': '#F6F6F6'}))
        ])
        return pn.WidgetBox(*self.panels, scroll=True)


    def clr_history(self,count=0):
        self.chat_history = []
        return 

cb = cbfs(tools)

inp = pn.widgets.TextInput( placeholder='Enter text here…')
#inp2 = pn.widgets.Button()

conversation = pn.bind(cb.convchain, inp) 

tab1 = pn.Column(
    pn.Row(inp),
    pn.layout.Divider(),
    pn.panel(conversation,  loading_indicator=True, height=400),
    pn.layout.Divider(),
)

dashboard = pn.Column(
    pn.Row(pn.pane.Markdown('# QnA_Bot')),
    pn.Tabs(('Conversation', tab1))
)
dashboard