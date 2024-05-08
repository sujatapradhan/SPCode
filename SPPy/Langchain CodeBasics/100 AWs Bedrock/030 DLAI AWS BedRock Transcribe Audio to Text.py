#https://learn.deeplearning.ai/courses/serverless-LLM-apps-amazon-bedrock/lesson/3/summarize-an-audio-file
# could not complete as s3 and transcribe services not avlabe
'''
Summarize Audio (Audio)
'''

#======================================================================================================
# STEP 00. Set up
print("Start-------------------------------------")
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]


#======================================================================================================
# STEP 00. AWS Set up
import boto3   #AWS
import json
import boto3_helpers

#======================================================================================================
# STEP 10. Set up loggig on AWS loudwatch
"""
'''
Authorize your application to send data to AWS
Create an app monitor
Create a log stream within a log group
Send logs to the created log stream
Insert the code snippet into your application
Test your app monitor setup by generating user events 
'''
#from helpers.CloudWatchHelper import CloudWatch_Helper
import boto3_helpers.cloudwatch
from boto3_helpers.pagination import yield_all_items
cloudwatch = CloudWatch_Helper()
cloudwatch = boto3_helpers.cloudwatch()  
#cloudwatch = cloudwatch #CloudWatch_Helper()
log_group_name = '/my/amazon/bedrock/logs'      # AWS IAM permission Allow logs:CreateLOgSTrem and logs:PutLogEvents 
                                                # and put trust plicy for bedroc service
cloudwatch.create_log_group(log_group_name)



bedrock = boto3.client('bedrock', region_name="us-west-2")
os.environ['LOGGINGROLEARN']='arn:aws:iam::653653134487:role/c99355a2566044l6607716t1w65365313448-LoggingIAMRole-d3vWHT2FmDUV'
os.environ['LOGGINGBUCKETNAME']='c99355a2566044l6607716t1w653653134-loggings3bucket-jj1ufpuihp4f'
loggingConfig = {
    'cloudWatchConfig': {
        'logGroupName': log_group_name,
        'roleArn': os.environ['LOGGINGROLEARN'],
        'largeDataDeliveryS3Config': {
            'bucketName': os.environ['LOGGINGBUCKETNAME'],
            'keyPrefix': 'amazon_bedrock_large_data_delivery',
        }
    },
    's3Config': {
        'bucketName': os.environ['LOGGINGBUCKETNAME'],
        'keyPrefix': 'amazon_bedrock_logs',
    },
    'textDataDeliveryEnabled': True,
}
bedrock.put_model_invocation_logging_configuration(loggingConfig=loggingConfig)
'''
#faiule das I dont have the role arn and bucket
#AccessDeniedException: An error occurred (AccessDeniedException) when calling the PutModelInvocationLoggingConfiguration operation: Cross-account pass role is not allowed.
'''
bedrock.get_model_invocation_logging_configuration()

#Every time the call to watch globally calls to Bedrck 
cloudwatch.print_recent_logs(log_group_name)
#Or in AWS COnsoel 
# Search CloudWatch->Logs->Log Groups-> Look at log streams of Log Groups
"""

# =========================================================================================
# STEP 20. Get teh recording
from IPython.display import Audio
audio = Audio(filename="../../res/download.mp3")
display(audio) # diplay control to paly and download audio
''' download , did not need it as tripple dot gave download option
with open('../../res/myfile.mp3', 'wb') as f:
        f.write(audio.data)
        f.close
'''

# just for inference #bedrock = boto3.client('bedrock-runtime', region_name='us-east-1') #region_name='us-west-2')
transcribe_client = boto3.client('transcribe', region_name='us-east-1') #region_name='us-west-2')

local_audio_path = "../../res/download.mp3" #"/path/to/your/local/audio.wav"
def transcribe_local_file(job_name, local_audio_path, transcribe_client):
    
    with open(local_audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = Audio(filename=local_audio_path)

    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": str(audio)},
        MediaFormat="mp3",
        LanguageCode="en-US",
    )

'''
transcribe_local_file("my-transcription-job", local_audio_path, transcribe_client)

# FAILED - 12 months free packge wil give TRanscribe free
# error 
# User: arn:aws:iam::837071794782:user/shreenivas.madagundi@atos.net 
# is not authorized to perform: transcribe:StartTranscriptionJob 
# on resource: arn:aws:transcribe:us-east-1:837071794782:transcription-job/my-transcription-job 
# because no identity-based policy allows the transcribe:StartTranscriptionJob action
'''


'''
#using buckets wil need s3 service and transcribe - both free for 12 months
s3_client = boto3.client('s3',  region_name='us-east-1') # region_name='us-west-2')
bucket_name = 'c99355a2566042l6607040t1w570359123-learners3bucket-2sxigj4ccsza' #os.environ['BucketName']
file_name = local_audio_path #'dialog.mp3'
s3_client.upload_file(file_name, bucket_name, file_name)  # upload from local file to same file name in bucket
'''

# could not complete as s3 and transcribe services not avlabe
#load json text manually 
with open('../../res/transcript_manual.txt', "r") as file:
    transcript_text  = file.read()

'''
# could not complete as s3 and transcribe services not avlabe
import uuid
job_name = 'transcription-job-' + str(uuid.uuid4())
response = transcribe_client.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': f's3://{bucket_name}/{file_name}'},
    MediaFormat='mp3',
    LanguageCode='en-US',
    OutputBucketName=bucket_name,
    Settings={
        'ShowSpeakerLabels': True,
        'MaxSpeakerLabels': 2
    }
)

#loop to wait for transcription to finish
while True:
    status = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    time.sleep(2)
print(status['TranscriptionJob']['TranscriptionJobStatus'])

# write to file
txt_file_path = '../../dialog.txt'


#for s3 #if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
if 'COMPLETED'== 'COMPLETED':
    #txt_file_path = f'{job_name}.txt' # for s3
    # Load the transcript from S3.
    transcript_key = f"{job_name}.json"
    transcript_obj = s3_client.get_object(Bucket=bucket_name, Key=transcript_key)
    transcript_text = transcript_obj['Body'].read().decode('utf-8')

'''
transcript_json = json.loads(transcript_text)
#print(json.dumps(transcript_json, indent=3))
output_text = ""
current_speaker = None

items = transcript_json['results']['items']

for item in items:
    
    speaker_label = item['speaker_label'] #OR # item.get('speaker_label', None)
    content = item['alternatives'][0]['content']
    #print(speaker_label + " : "+content)
    # Start the line with the speaker label:
    if speaker_label is not None and speaker_label != current_speaker:
        current_speaker = speaker_label
        output_text += f"\n{current_speaker}: "
        
    # Add the speech content:
    if item['type'] == 'punctuation':
        output_text = output_text.rstrip()
        
    output_text += f"{content} "

#print  (output_text)
    

##################################################################################
# Save the transcript to a text file 
#S3 #txt_file_path=f'{job_name}.txt' 
# write to file
txt_file_path = '../../res/from_transcript_manual.txt'
with open(txt_file_path, 'w') as f:
    f.write(output_text)
    f.close





##################################################################################
#S3 #txt_file_path=f'{job_name}.txt' 
txt_file_path = '../../res/from_transcript_manual.txt'
#read teh transcript from a file
with open(txt_file_path, "r") as file:
    transcript = file.read()
    

################################################################################################
### USE JINJA for PROD env to sperate version cotrolled PROMPT files########################
"""
#using pynb cells to creat ethe file.... 
%%writefile ../../res/prompt_template.txt
Human: I need to summarize a conversation. The transcript of the 
conversation is between the <data> XML like tags.

<data>
{{transcript}}
</data>

The summary must contain a one word sentiment analysis, and 
a list of issues, problems or causes of friction
during the conversation. The output must be provided in 
JSON format shown in the following example. 

Example output:
{
    "sentiment": <sentiment>,
    "issues": [
        {
            "topic": <topic>,
            "summary": <issue_summary>,
        }
    ]
}

Write the JSON output and nothing more.

Assistant: Here is the JSON output:

"""

###############################################################################
# use Jija as teh templating library
from jinja2 import Template
#S3 #prompt_file_path=f'{job_name}.txt' 
prompt_file_path = '../../res/prompt_template.txt'
#read teh transcript from a file
with open(prompt_file_path, "r") as file:
    template_string = file.read()

data = {
    'transcript' : transcript
}
template = Template(template_string)
prompt = template.render(data)
print(prompt)


#modelId="amazon.titan-text-express-v1"
modelId="anthropic.claude-v2:1"
accept="application/json"
contentType="application/json"

#the prompt I had to modify wiyj Human and Assistant (becasuse it is claude???

body= json.dumps({
    'prompt':prompt,
    'max_tokens_to_sample':1024,
    "top_p":0.8,
    "temperature":0,                 #to get json right
})


kwargs = {
    "modelId": modelId,
    "contentType": "application/json",
    "accept": "*/*",
    "body": body
}


#bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')
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
