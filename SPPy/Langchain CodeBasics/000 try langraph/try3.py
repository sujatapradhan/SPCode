
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]



import requests
import json

# DuckDuckGo API endpoint
ddg_api_url = "http://api.duckduckgo.com/"

# Search query
search_query = "Capital of India"

# Parameters for the API request
params = {
    "q": search_query,
    "format": "json",
    "pretty": "1"
}

# Make the API request
response = requests.get(ddg_api_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)
    print(json.dumps(data, indent=2))
    
    # Extract the relevant information
    abstract = data.get("Abstract", "")
    redirect_url = data.get("Redirect", "")
    
    print(f"Abstract: {abstract}")
    print(f"Redirect URL: {redirect_url}")
else:
    print(f"Error: {response.status_code} - {response.text}")
