# https://www.youtube.com/watch?v=I4RQVAbsKWY&t=170s

import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.agents import AgentExecutor, create_react_agent, create_json_agent, create_structured_chat_agent

#deprecated #from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
llm=ChatOpenAI(temperature=0, model="gpt-4")
#tools=load_tools(["serpapi", "llm-math"], llm=llm)
tools=load_tools(["ddg-search"], llm=llm)

q="What is the capital of India?"
# derepacted  # BUT ok
'''
agent=initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)#, verbose=True)
agent.run(q)
'''

from langchain.agents import load_tools, AgentExecutor, create_react_agent

prompt = hub.pull("hwchase17/react")
from langchain_core.prompts import PromptTemplate

template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)


#model = OpenAI()
model =ChatOpenAI(temperature=0, model="gpt-4")
tools=load_tools(["serpapi", "llm-math"], llm=llm)
#tools=load_tools(["ddg-search"], llm=model)


agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

q="What is the capital of India?"
q="What is the cube root of 125 squared?"
agent_executor.invoke({"input": q},verbose=True)



# Use with chat history
from langchain_core.messages import AIMessage, HumanMessage
agent_executor.invoke(
    {   "input": "what's my name?",
        # Notice that chat_history is a string 
        # since this prompt is aimed at LLMs, not chat models
        "agent_scratchpad": '''Human: My name is Bob
                         AI: Hello Bob!
                         Human: I live in Mumbai
                         AI: That's nice''',
    }
    )
print(prompt)
    


# Create a JSON agent #agent = create_json_agent(json_file_path)

# Create a structured chat agent #agent = create_structured_chat_agent(chat_data_path)

# Create a React agent
agent = create_react_agent(agent_prompt)