from langchain.agents import tool 
from pydantic.v1 import BaseModel, Field

@tool
def search_wikipedia():
    """search_wikipedia"""
    print("search_wikipedia")
@tool
def get_current_temperature():
    """get_current_temperature"""
    print ("get_current_temperature")
    
toolsDict = {   "search_wikipedia": search_wikipedia, 
                "get_current_temperature": get_current_temperature}


#from langchain_openai import ChatOpenAI
#functions = [convert_to_openai_function(f) for fname,f in toolsDict.items()]
#model = ChatOpenAI(temperature=0).bind(functions=functions)

#DeprecationWarning #from langchain.chat_models import ChatOpenAI 
#DeprecationWarning #from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

class TooledChatOpenAI(ChatOpenAI):
    def __init__(self, temperature, toolsDict):
        super().__init__(temperature=temperature)
        self.toolsDict = toolsDict

    def invoke(self, query):
        # Check if the query matches any custom function
        for fname, f in self.toolsDict.items():
            if query.lower() == query.lower():
                # Execute the custom function
                f()
                return

        # If not a custom function, use the base invoke method
        return super().invoke(query)

# Create an instance of your custom model
model = TooledChatOpenAI(temperature=0, toolsDict=toolsDict)

# Now you can invoke your custom functions
query = "what is the weather in San Francisco right now?"
model.invoke(query)

query = "what is LangChain?"
model.invoke(query)

query = "Hi"
model.invoke(query)