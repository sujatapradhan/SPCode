#https://www.youtube.com/watch?v=zdwYHg9CEvg
'''
LangChain 🦜 ~ Free Web Search
======================================================================
Objectives :
1. Langchain is bad at maths
----------------------------
Let's prove it
Let's fix it

2. SERPAPI needs tokens (Does it?) -- duckduckgo search is free
-----------------------
We can avoid it

3. Solve a deprecation warning for LLMMathChain
-----------------------------------------------
New Syntax
'''

#!pip install duckduckgo-search
print("================================================================================================================================================================================================================================")

# 1) Imports ######################################~~
import os
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

#decrecated #from langchain.llms import OpenAI
#decrecated #from langchain_community.llms import OpenAI
from langchain_openai import OpenAI
from langchain.agents import Tool, initialize_agent
#deprecated #from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
#deprecated #from langchain.tools import DuckDuckGoSearchRun
from langchain_community.tools import DuckDuckGoSearchRun
#deprecated #from langchain.utilities import WikipediaAPIWrapper
from langchain_community.utilities import WikipediaAPIWrapper
#deprecated #from langchain import OpenAI, LLMMathChain
from langchain.chains import LLMMathChain

from langchain.chains import LLMChain
from langchain.agents.agent_types import AgentType


# 2) LLM ##################################################
llm = OpenAI(temperature=0)

# 3) Tools ##################################################

search = DuckDuckGoSearchRun()
wikipedia = WikipediaAPIWrapper()


# Web Search Tool
search_tool = Tool(
    name="Web Search",
    func=search.run,
    description="A useful tool for searching the Internet to find information on current events, years, dates, issues, etc. Worth using for general topics. Use precise questions.",
)

# Wikipedia Tool
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia.run,
    description="A useful tool for searching the Internet to find information on world events, issues, dates, years, etc. Worth using for general topics. Use precise questions.",
)


#deprecated #from langchain import LLMMathChain
from langchain.chains import LLMMathChain

#llm_math_chain = LLMMathChain(llm=llm, verbose=True) <- Deprecated !!!

llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
math_tool = Tool.from_function(
        func=llm_math_chain.run,
        name="Calculator",
        description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions.",
    )


# 4) Agent ##################################################
query = "search for King Charles' current age in years and then calculate the cube root of that number to 1 decimal"
tools = [search_tool,wikipedia_tool,math_tool]

# deprecated 
'''
agent = initialize_agent(
    tools = tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  
)

##Run
agent.run(query)
'''

# Use new agent constructor methods instead, like:
# create_react_agent, create_json_agent, create_structured_chat_agent, etc.

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
Thought:{agent_scratchpad}
'''

'''
or DO IT FROM messages
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful but sassy assistant"),
    MessagesPlaceholder(variable_name="chat_history"),      # add for chat History and ensure has it in Runnable pass through
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")    # add extra MessagesPlaceholder line for  Tool call history to pass list of messages
])
'''


agent_prompt = PromptTemplate.from_template(template)
#agent_prompt = hub.pull("hwchase17/react-chat")
from langchain.agents import AgentExecutor, create_react_agent
agent = create_react_agent(llm, tools, agent_prompt)
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
agent_executor = AgentExecutor(agent=agent, tools=tools) #, memory=memory)

#deprecated #agent.run(query)
query = "what's my name?"
query = "search for King Charles' current age in years and then calculate the cube root of that number to 1 decimal"
#query = "what is the date today in India"
response=agent_executor.invoke(
    {
        "input": query,
        # Notice that chat_history is a string
        # since this prompt is aimed at LLMs, not chat models
        "chat_history": '''Human: My name is Bob
AI: Hello Bob!
''', 
        "verbose":"True"
})
print(response)
