########Set up env variables in main##############################
import os    # Access to env varibales
from dotenv import find_dotenv, load_dotenv # Set up to read API keys from .env #install python-dotenv
#load_dotenv(../.env) # if outside project folder
load_dotenv() # find_dotenv wil find teh .env up te parent path # now you have access to os.environ[HUGGINGFACEHUB_API_TOKEN]
#print("Hello ",os.environ["HUGGINGFACEHUB_API_TOKEN"])

import langchainFuncs as lf   # local module
p1 = lf.Person("John", 36)
print (p1) # p1 __str__ is used
print (p1.myfunc())

#ref  https://www.youtube.com/watch?v=nAmC7SoVLd8

########Set streamlit to run your test page##############################
import streamlit as st
import langchainFuncs as lf   # local module
st.write("Hello from Streamlit")
st.title("XXX 0.2")
cuisine=st.sidebar.selectbox("Pick a cuisine",("","Italian","Indian","Mexian","Arabian"))

#if 'myButton' not in st.session_state:
#    st.session_state.myButton = False
#def click_myButton():
#    st.session_state.agentButton = not st.session_state.agentButton

agentButton=st.sidebar.button('Agent') #, on_click=click_myButton)
if agentButton:
    cuisine=None
    st.header("SOmething else")
    st.write("*****Else***")
    

if cuisine:
    response = lf.spCuisine(cuisine,5)
    
    st.header(response['name'].strip())
    st.write("*****Menu***")
    menu=response['menu'].strip().split("\n")
    
    
    for i in menu:
        st.write("-",str(i).strip())
    
    
    ### for json returns
    #import json # Python program to convert JSON to Python
    #res =response['menu'].strip()                   # '{"id":"09", "name": "Nitin", "department":"Finance"}' # JSON string
    #res_dict = json.loads(res)                      # Convert string to Python dict
    #print(res_dict['name'])
    #print(res_dict) 
    
    
    
    st.write("\n\n\n")
    st.write(response)