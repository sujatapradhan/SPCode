#https://python.langchain.com/v0.1/docs/integrations/tools/ddg/
#from langchain_community.tools import DuckDuckGoSearchTool
from langchain_community.tools import DuckDuckGoSearchRun
#from langchain_community.tools import DuckDuckGoSearchResults
#from langchain_community.tools import DuckDuckGoSearchResults


search=DuckDuckGoSearchRun()
search.run('Capital of India')