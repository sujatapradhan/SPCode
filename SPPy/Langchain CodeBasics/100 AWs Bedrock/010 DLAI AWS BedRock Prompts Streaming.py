
#https://learn.deeplearning.ai/courses/serverless-LLM-apps-amazon-bedrock/lesson/2/your-first-generations-with-amazon-bedrock
#Working

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
#print("Hello ",os.environ["AWS_ACCESS_KEY_ID"])          
#print("Hello ",os.environ["AWS_SECRET_ACCESS_KEY"])
#OR in google colab add Key as secret. GROQ_API_KEY. 
# from google.colab import userdata # and access it as userdata.get('GROQ_API_KEY')

import boto3   #AWS
import json

#bedrock=boto3.client(service_name='bedrock-runtime',region_name='us-east-1') #'us-west-2')
#bedrock_runtime =
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1') #region_name='us-west-2')

####
prompt='<s>[INST] Which one came first? Egg or Chicken? [/INST]</s>'
prompt='Which one came first? Egg or Chicken?'
prompt = "Write a one sentence summary of Las Vegas."
prompt = "Write a summary of Las Vegas."

#modelId="mistral.mixtral-8x7b-instruct-v0.1"
#modelId="anthropic.claude-3-sonnet-20240229-v1:0"
#modelId="amazon.titan-text-lite-v1"
modelId="anthropic.claude-v2:1"
accept="application/json"
contentType="application/json"

#the prompt I had to modify wiyj Human and Assistant (becasuse it is claude???

body= json.dumps({
    'prompt':"""

Human:""" + prompt+"""

Assistant:""",
    'max_tokens_to_sample':100,
    "top_p":0.8,
    "temperature":0.5,
})


kwargs = {
    "modelId": modelId,
    "contentType": "application/json",
    "accept": "*/*",
    "body": body
}


response = bedrock.invoke_model(**kwargs)
#print(response)

'''#either steream
for streamingChunks in response["body"]:
  print(streamingChunks,end="\n"),
print("\n")
'''

# or
response_body = json.loads(response.get('body').read())
print(json.dumps(response_body, indent=4))
### valid only in DLAI sandbox  # print(response_body['results'][0]['outputText'])
print(response_body['stop_reason']) 
print(response_body['completion'])
