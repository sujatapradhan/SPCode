import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]

from serpapi import GoogleSearch
import json
params = {
  "engine": "duckduckgo",
  "q": "Capital of India",
  "kl": "us-en",
  "api_key": os.environ["SERPAPI_API_KEY"]
}

search = GoogleSearch(params)
results = search.get_dict()
print(json.dumps(results,indent=4))