# https://www.youtube.com/watch?v=0xyXYHMrAP0&t=9s

print("Start-------------------------------------")
###### Set up Subdirectiry package importing 
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #SO that subdir package import works

########Set up env variables in main##############################
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]
#----------------------------------------------------------------------------------------------------------------------------------

EIther
import sagemaker
from sagemaker.huggingface import (
    HuggingFaceModel,
    get_huggingface_llm_image_uri
)

role = sagemaker.get_execution_role()

hub_config = {
    'HF_MODEL_ID':'meta-llama/Llama-2-7b', # model_id from hf.co/models
    'HF_TASK':'text-generation' # NLP task you want to use for predictions
}

# retrieve the llm image uri
llm_image = get_huggingface_llm_image_uri(
    "huggingface",
    version="0.8.2"
)

my_model = HuggingFaceModel(
    env=hub_config,
    role=role, # iam role with permissions to create an Endpoint
    image_uri=llm_image
)

#----------------------------------------------------------------------------------------------------------------------------------
