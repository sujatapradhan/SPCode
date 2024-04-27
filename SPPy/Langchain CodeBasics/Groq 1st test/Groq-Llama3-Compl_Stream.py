print("Start-------------------------------------")
###### Set up Subdirectiry package importing 
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works
from spCommons.spTimer import spTimer as st # st.ShowTime 
#import spCommons.spTimer as st   # st.spTimer.ShowTime and st.directShowTime


    

@st.ShowTime
def doCompl(query, sysMsg, stream, client, model):
    ########Set up env variables in main##############################
    import os    # Access to env varibales
    from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
    #load_dotenv(../.env) # if outside project folder
    load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]
    #print("Hello ",os.environ["HUGGINGFACEHUB_API_TOKEN"])
    #OR in google colab add Key as secret. GROQ_API_KEY. 
    # from google.colab import userdata # and access it as userdata.get('GROQ_API_KEY')
    
    # https://www.youtube.com/watch?v=ySwJT3Z1MFI
    #!pip install -q groq
    #from groq import Groq as llm1
    #client=llm (api_key=key)
    # there can be chat (playground),, completion (q n a), instruction types
    chat_completion = client.chat.completions.create(
        messages = [
            {"role":"system", 
            "content": sysMsg,
            },
            {"role":"user", 
            "content": query,
            }
        ],
        model=model,
        temperature=1,
        top_p=.51, #control diversity vaia nucleus sampling. 0.5 means half of all likelihood-weighted options are considered. 
        max_tokens=1024,
        stop=None, # to stop generating can be [end] or punctuation marks
        stream=stream, #for long responses
        #tools=tools,
        #tool_choice="auto",  # auto is default, but we'll be explicit
        
    )
    
    if not stream:
        #For strem=False
        print(chat_completion.choices[0].message.content)
    else:
        #For stream=True handle chunks
        for streamingChunks in chat_completion:
            print(streamingChunks.choices[0].delta.content,end=""),
        print("\n")
    print("Inference Engine:" + str(type(client)) + "   Model:" + model)
            
#set llm and Key
from groq import Groq as llm1
client=llm1 (api_key=os.environ['GROQ_API_KEY'])
model="llama3-70b-8192"

'''
from openai import OpenAI as llm1
client=llm1(api_key=os.environ['OPENAI_API_KEY'])
model="gpt-3.5-turbo-0125"
'''
sysMsg="You are a helpful assistant. Answer in json."
sysMsg="You are a helpful assistant. Answer as John Snow from Game of Thrones."

q = "Explain teh importance of low latency LLMs. Explain it in teh voice of John Snow."
q="WHat's the capital of India? Write a detailed essay about it." #or
q="WHat's the capital of India?"

doCompl(query=q,sysMsg=sysMsg,stream=True,client=client,model=model)
print("End-------------------------------------")
