print("Start-------------------------------------")
###### Set up Subdirectiry package importing 
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works
#from spCommons.spTimer import spTimer as st # st.ShowTime 
##import spCommons.spTimer as st   # st.spTimer.ShowTime and st.directShowTime

########Set up env variables in main##############################
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
#load_dotenv(../.env) # if outside project folder
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]
print("Hello ",os.environ["AWS_ACCESS_KEY_ID"])          
print("Hello ",os.environ["AWS_SECRET_ACCESS_KEY"])
#OR in google colab add Key as secret. GROQ_API_KEY. 
# from google.colab import userdata # and access it as userdata.get('GROQ_API_KEY')

import boto3   #AWS
import json

bedrock=boto3.client(service_name='bedrock-runtime',region_name='us-east-1') #'us-west-2')
####
prompt='<s>[INST] Which one came first? Egg or Chicken? [/INST]</s>'
prompt='Which one came first? Egg or Chicken?'
body= json.dumps({
    'prompt':prompt,
    'max-tokens':512,
    "top_p":0.8,
    "temperature":0.5,
})


import json
#print(json.dumps(msg))

q="Answer in one word. What is the capital of Australia?"
anthropic_version= "bedrock-2023-05-31"
max_tokens=512
temperature=0
top_k=1
top_p=0.1

json='''
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "''' + q + '''"
        }
      ]
    }
  ],
  "anthropic_version": "''' + anthropic_version + '''",
  "max_tokens": '''+ str(max_tokens) +''',
  "temperature": '''+ str(temperature) +''',
  "top_k": '''+ str(top_k) +''',
  "top_p": '''+ str(top_p) +''',
  "stop_sequences": [
    "\\n\\nHuman:"
  ]
}'''
#json='Which one came first? Egg or Chicken?'
#modelId="mistral.mixtral-8x7b-instruct-v0.1"
#modelId="anthropic.claude-3-sonnet-20240229-v1:0"
modelId="anthropic.claude-v2:1"
accept="application/json"
contentType="application/json"

response = bedrock.invoke_model(
    body=json,
    modelId=modelId,
    accept=accept,
    contentType=contentType
) 
import json
body=json.loads(response.get('body').read().decode())     # decode: Convert bytes/streamed strings to a string - can also specify  encoding: srtObj = byteObj.decode('utf-8')

print(type(body))
print(body["content"][0]["text"])
json.dumps(body)