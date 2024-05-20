# duckDuckGo
# https://www.youtube.com/watch?v=W3Dq4LIr6h4
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]


import pandas as pd
from duckduckgo_search import DDGS

"""
Args: 
    keywords: keywords for query.
    # https://duckduckgo.com/duckduckgo-help-pages/settings/params/
    region: wt-wt, us-en, uk-en, ru-ru etc default to wt-wt
    safesearch: on,moderate, off. defaults to moderate
    timelimit: d,w,m,y. defaulst to None
    backend: api, html, lite. defaults to api
        api - collects data from https://duckduckgo.com
        html - from https://html.duckduckgo.com
        lite - from https://lite.duckduckgo.com
    max_results: max number of results. defautls to None and returns first only         
"""

'''import backoff
import requests

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
def search_duckduckgo(query):
    params = {
        "q": query,
        "format": "json",
        "pretty": "1",
        "max_results": 1
    }
    response = requests.get("http://api.duckduckgo.com/", params=params)
    response.raise_for_status()
    return response.json()

'''
model = DDGS()
#model = DDGS(proxy="socks5://user:password@geo.iproyal.com:32325", 
#             timeout=20)
#results = model.text("something you need", max_results=50)
search_query = 'python tutorials'
results=model.text(keywords=search_query,
    region='en-us',
    safesearch='off',
    backend='api',
    max_results=1
    )
print(results)



'''
results = DDGS().text('live free or die', region='wt-wt', safesearch='off', timelimit='y', max_results=10)
# Searching for pdf files
results = DDGS().text('russia filetype:pdf', region='wt-wt', safesearch='off', timelimit='y', max_results=10)

# async
results = await AsyncDDGS().text('sun', region='wt-wt', safesearch='off', timelimit='y', max_results=10)
'''
#use proxy with ddgs
results = DDGS(proxy="socks5://user:XXXXXXXXXXXXXXXXXXXXXXXX:32325",
               timeout=20).text('sun', region='wt-wt', safesearch='off', 
                                timelimit='y', max_results=10)

