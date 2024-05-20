print("Start-------------------------------------")
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works #from spCommons.spTimer import spTimer as st # st.ShowTime 
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]

import openai
openai.api_key=os.environ["AZURE_OPENAI_API_KEY"]
openai.api_type = "azure"
response = openai.chat.completions.create(engine="gpt-4",
                                        messages=[
                                            {"role":"system", "content":"You are a helpful assistant."},
                                            {"role":"user", "content":"Who won the world series in 2020?"},
                                            {"role":"assisstant", "content":"The LA DOdgers won the world series in 2020."},
                                            {"role":"user", "content":"Where was it played?"},  
                                        ]
                                        )

print("End-------------------------------------")
