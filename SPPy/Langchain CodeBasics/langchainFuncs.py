# https://www.youtube.com/watch?v=nAmC7SoVLd8
######################################
#Set up to read  API keys from .env
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv()   # find_dotenv wil find teh .env up te parent path
#print("Hello","there")

def spCuisineMock(cuisine):
    return {'cuisine': 'Mexican', 
            'name': 'Casa del Sabor de México (House of Mexican Flavor)', 
            'menu': ' 1. Tacos, 2. Burritos, 3. Enchiladas \n20. Agua Fresca.'}
    return { "name":cuisine,
                "menu": 'asmosa,ice'}
def test(q):
    oak=os.environ["OPENAI_API_KEY"]
    #from langchain.llms import OpenAI
    from langchain_community.llms import OpenAI 
    llm=OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.6) #pass api_key= or reads env
    #llm=OpenAI(model="gpt-4-turbo", temperature=0.6) #pass api_key= or reads env
    
    out=llm.predict(q)
    print("\n\n\n==============\nFrom OpenAI\nQuestion:", q, "   \nAnswer:",out)

    hfk=os.environ["HUGGINGFACEHUB_API_TOKEN"]
    repo="google/flan-t5-large"
    #from langchain.llms import OpenAI
    from langchain_community.llms import HuggingFaceHub
    llm_hf = HuggingFaceHub(repo_id=repo, model_kwargs={"temperature":0, "max_length":64})

    out_hf= llm_hf.predict(q)
    
    print("\n\n\n==============\nFrom HF\nQuestion:", q, "   \nAnswer:",out_hf)
    return out_hf


def spCuisine(cuisine, count):
    ######################################
    #PROMPT TEMPLATES
   
    oak=os.environ["OPENAI_API_KEY"]
     
    # from langchain.llms import OpenAI  #deprecated
    # from langchain_community.llms import OpenAI #deprecated 
    from langchain_openai import OpenAI 
    llm=OpenAI(temperature=1) #pass api_key= or reads env, also model="gpt-3.5-turbo-instruct"
    from langchain.globals import set_debug
    #set_debug(True)
    
    #from langchain.prompts import PromptTemplate
    from langchain_core.prompts import PromptTemplate
    
    #pt=PromptTemplate(input_variables=['cuisine'], 
    #                  template='Suggest a fancy name for a {cuisine} restaurant.') 
    #test format   pt.format(cuisine="Indian") 
    from langchain.chains import LLMChain
    chnName=LLMChain(llm=llm,
                prompt=PromptTemplate(input_variables=['cuisine'],
                                    template='Suggest a fancy name for a {cuisine} restaurant.')
                ,output_key="name",
                )
    #for plain chain.run or SimpleSequentialChain # out=chn.run(cuisine)
    #print(out)

    chnMenu=LLMChain(llm=llm, 
                prompt=PromptTemplate(input_variables=['name','count'], 
                                        template='''Suggest a list of {count} menu items and their descriptions for  {name} restaurant. 
                                        Your output should be returned in a in a format as listed below within ` marks below:
                                            `1. Rice: An aromatic rice dish; 
                                            2. Dal: Lentils slow cooked in Indian spices;
                                            3. Butter Chicken: A mouthwatering chicken dish;
                                            4. Matar Paneer: A vegetarian sumptuous delight`
                                        ''')
                ,output_key="menu"
                )
    #for plain chain.run or SimpleSequentialChain# out=chn2.run(out)
    #print(out)
    
    #But youcan chain them without middle outputs, and each can take only one input. 
    '''from langchain.chains import SimpleSequentialChain 
    finchn = SimpleSequentialChain( chains=[chnName,chnMenu])
    response=finchn.run(cuisine)
    return response
    '''
    #But youcan chain them with without middle outputs 
    from langchain.chains import SequentialChain #Uses the output_key
    finchn =  SequentialChain( chains=[chnName,chnMenu], 
                            input_variables=['cuisine','count'],
                            output_variables=['name','menu'],verbose=True)
    response=finchn({"cuisine":cuisine,'count':count})

    #print(response) 
    return response

#def get_word_length(word: str) -> int:
#    """Returns the length of a word."""
#    return len(word)

def spAgent(q):
    ######################################
    #PROMPT TEMPLATES
   
    oak=os.environ["OPENAI_API_KEY"]
     
    # from langchain.llms import OpenAI  #deprecated
    # from langchain_community.llms import OpenAI #deprecated 
    from langchain_openai import OpenAI 
    #llm=OpenAI(model="gpt-4-turbo", temperature=0) #pass api_key= or reads env, also model="gpt-3.5-turbo-instruct"
    llm=OpenAI(model="gpt-3.5-turbo-instruct", temperature=0.6) #pass api_key= or reads env
    
    from langchain.agents import AgentType, initialize_agent, load_tools
    tools=load_tools(["wikipedia"],llm=llm)               #https://python.langchain.com/docs/integrations/tools/
    #TODO https://towardsdatascience.com/building-a-math-application-with-langchain-agents-23919d09a4d3
    agent=initialize_agent(tools,llm,agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,handle_parsing_errors=True,verbose=True)                                        
    response=agent.run(q)                                        

    #get_word_length.invoke("abc")
    
    #response=""
    return response


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        #from datetime import datetime #dataetime
        dt_string = "datetime not working " #datetime.now().strftime("%d%b%y %H:%M:%S")
        return f"{dt_string} :  {self.name} - (age:{self.age})"
    def myfunc(self):
        return "Hello my name is " + self.name

if __name__ == "__main__":
    print("Directly called")
    #set question
    #print("\n\n\n==============\nHF\nQuestion:", q, "   \nAnswer:",test(q))
    #print(spCuisineMock("Mexican"))
    
    #from datetime import datetime #dataetime
    dt_string = "datetime not working "; #datetime.now().strftime("%d%b%y %H:%M:%S")
    print(dt_string, spCuisine("Arabian",2))
    
    q="what is the area of capital of India?"
    print(spAgent(q))
else:
    pass



