#Not Working
# #https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/2/openai-function-calling
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

import json
# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return "json.dumps(weather_info)"
print(get_current_weather('{\n  "location": "Boston,MA"\n}'))

# define a function
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]
messages = [
    {
        "role": "user",
        "content":"What's the weather like in Boston?"   # "How far away is the moon?" #
    }
]
# Was deprecated so used https://community.openai.com/t/chatcompletion-issues-can-anyone-help/479462/6

'''import openai
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=functions
)
'''

'''
#this worked from https://community.openai.com/t/chatcompletion-issues-can-anyone-help/479462/6

from openai import OpenAI
client = OpenAI()
def get_completion(prompt, client_instance, functions, model="gpt-3.5-turbo"):
  messages = [{"role": "user", "content": prompt}]
  response = client_instance.chat.completions.create(
  model=model,
  messages=messages,
  functions=functions,
  max_tokens=50,
  temperature=0,
  )
  return response.choices[0].message.content
prompt = "What's the weather like in Boston?" #"How far away is the moon?"
response = get_completion(prompt, client, functions, model="gpt-3.5-turbo-0613") # call your function
'''
# so chnaged to 
import openai
response = openai.chat.completions.create(
    model="gpt-4-turbo-preview", #"gpt-3.5-turbo-0125", # "gpt-3.5-turbo-0613",
    messages=messages,
    functions=functions
)

print("response")
print("--------------------------------------------")
print(type(response))
print(response)

content=response.choices[0].message.content
print("response.choices[0].message.content")
print("--------------------------------------------")
print(type(content))
print(content)

#response_message = response["choices"][0]["message"]



