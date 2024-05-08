
#https://learn.deeplearning.ai/courses/serverless-LLM-apps-amazon-bedrock/lesson/2/your-first-generations-with-amazon-bedrock
# Parts 2
'''
Working with other type of data (Audio)
'''

print("Start-------------------------------------")
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]

import boto3   #AWS
import json
from IPython.display import Audio
audio = Audio(filename="../../res/download.mp3")
display(audio)
''' download , did not need it as tripple dot gave download option
with open('../../res/myfile.mp3', 'wb') as f:
        f.write(audio.data)
        f.close
'''
#redaing a file does not exist rigt now a sample only
with open('../../res/dialogue.txt', "r") as file:
    dialogue_text = file.read()
print(dialogue_text)


prompt = f"""
Human: The text between the <transcript> XML tags is a transcript of a conversation. 
Write a short summary of the conversation.

<transcript>
{dialogue_text}
</transcript>

Assistant: Here is a summary of the conversation in the transcript:"""



modelId="anthropic.claude-v2:1"
accept="application/json"
contentType="application/json"

#the prompt I had to modify wiyj Human and Assistant (becasuse it is claude???

body= json.dumps({
    'prompt':prompt,
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


bedrock = boto3.client('bedrock-runtime', region_name='us-east-1') #region_name='us-west-2')
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
