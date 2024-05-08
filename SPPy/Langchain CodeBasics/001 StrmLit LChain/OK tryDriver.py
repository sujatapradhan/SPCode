# https://www.linkedin.com/pulse/memory-llm-agents-ilya-fastovets-pnvec/?trackingId=EaZpxSuhSrCqtoOVCTNsHg%3D%3D
# working
#--------------------------------------------------------------------------------------------------------------------------
print("Start ================================================================================================================================================================================================================")
#--------------------------------------------------------------------------------------------------------------------------
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
#load_dotenv(../.env) # if outside project folder
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]
#print("Hello ",os.environ["HUGGINGFACEHUB_API_TOKEN"])
#--------------------------------------------------------------------------------------------------------------------------
import requests
from pydantic.v1 import BaseModel, Field               #Langchain doe snot support v2 yet
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.memory import ConversationSummaryBufferMemory
from langchain.tools import StructuredTool
import json
#--------------------------------------------------------------------------------------------------------------------------
# Step - Define all tools typically with @tool and pydantic===================================================================
def get_weather_for_city(city_name: str, units: str="imperial") -> dict:
    """
    Fetches weather data for a specified city.

    Parameters:
    - city_name (str): The name of the city.
    - units (str): Units of measurement. "metric" for Celsius, "imperial" for Fahrenheit.

    Returns:
    - dict: Weather data for the city.
    """
    api_key = os.environ["OPEN_WEATHER_MAP_API_KEY"]
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city_name}&units={units}"

    response = requests.get(complete_url)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data"}
'''
#test
city_name = "San Francisco"
weather_data = get_weather_for_city(city_name)
print(json.dumps(weather_data, indent=3))
'''
#--------------------------------------------------------------------------------------------------------------------------
# Define Pydantic arguments schema for these methods
# To better convert Python functions to Langchain Tools, describe their inputs using Pydantic classes.
# Those will be passed together with the function as arguments to the Langchain method that creates Tools from Python functions.
# For some reason, Pydantic v2 is not yet supported by Langchain, note that Pydantic v1 is used here.

class GetWeatherForCityInput(BaseModel):
    """
    Pydantic schema for the get_weather function inputs.
    """
    city_name: str = Field(..., description="The name of the city for which to fetch weather data.")
    units: str = Field(default="imperial", description="Units of measurement. Use 'metric' for Celsius or 'imperial' for Fahrenheit. Defaults to 'metric'.")
#--------------------------------------------------------------------------------------------------------------------------
# Step Define prompts ------------------------------------------------------------------------------------------------------------------------

system_init_prompt = """
You are a driving assistant capable of accessing weather data in any location. 
With this weather data, you provide detailed information about how safe it would be to drive in this location.
If two locations are provided, you also check two or three locations between them to make sure the entire road is good to drive.
"""
user_init_prompt = """
Chat history is: {}.
The question is: {}. 
Go!
"""
#--------------------------------------------------------------------------------------------------------------------------
# Step - Define parts of the agent using LCEL -------------------------------------------------------------------------------
# step 1) Initialize the LLM
llm = ChatOpenAI(
    temperature=0.5,
    model_name="gpt-4",
    #openai_api_key=os.environ["OPENAI_API_KEY"],
)

# Step 2) Initialize the memory: conversation summary buffer (out of main 4 types for chat) ----------------------------------------------------------------------------
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(
        model_name="gpt-3.5-turbo", # Use a cheaper model to summarize the history
        #openai_api_key=OPENAI_API_KEY,
    ),
    memory_key="chat_history", # What dict key to use to parse in the agent
    return_messages=True,
    max_token_limit=1024, # The bigger the limit, the more unsummarized messages
)


# step 3) Initialize the tools and bind to llm
tools = [
    StructuredTool.from_function(
        func=get_weather_for_city,
        args_schema=GetWeatherForCityInput,
        description="Function to get weather for specified city.",
    ), 
]
llm_with_tools = llm.bind(
    functions=[convert_to_openai_function(t) for t in tools]
)

# step 4) Initialize the prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_init_prompt),
        ("user", user_init_prompt.format("{chat_history}", "{input}")),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ],
)

# step 5) Finally Initialize agent  suing LCEL and teh agent executer
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

# Step 6) Initialize the agent executor
agent_executor = AgentExecutor(agent=agent, 
                               tools=tools, 
                               memory=memory,
                               verbose=True)

#--------------------------------------------------------------------------------------------------------------------------
# Now start teh bot at terminal-------------------------------------------------------------------------------------------------
print("Welcome to the chatbot. Type 'exit' to leave the chat.")

while True:
    user_message = input("You: ")
    if user_message.lower() == "exit":
        print("Exiting chat. Have a great day!")
        break

    response = agent_executor.invoke({"input": user_message})
    response = response.get("output")

    print(f"Chatbot: {response}")
'''
# Manually Test
You:  How safe is it to drive from San Francisco to Las Vegas? 
You:  Then I would like to proceed to New York
You:  So, summarize the whole trip
You:  Exit
'''
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------

print("End ==================================================================================================================================================================================================================")
