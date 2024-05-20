import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]

from langchain import hub
#from langchain_community.llms import OpenAI
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI

from langchain.agents import load_tools, AgentExecutor, create_react_agent

prompt = hub.pull("hwchase17/react")
#model = OpenAI()
model =ChatOpenAI(temperature=0, model="gpt-4")
tools=load_tools(["serpapi", "llm-math"], llm=llm)
#tools=load_tools(["ddg-search"], llm=model)


agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
q="What is the capital of India?"
q="What is the cube root of 125 squared?"
agent_executor.invoke({"input": q},verbose=True)