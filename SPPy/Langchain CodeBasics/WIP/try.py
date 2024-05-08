##########from app_Utils import switch_page
import streamlit as st  
from PIL import Image  
# im = Image.open("icon.png")  
##########im = Image.open("Eviden_RGB_BLack.png")  
##########st.set_page_config(page_title="AI Interviever", layout="centered", page_icon=im)  
# lan = st.selectbox("#### Language", ["English"])  
lan = "English"  
if lan == "English":  
    home_title = "AI Interviewer"  
    home_introduction = "Welcome to AI Interviewer, empowering your interview preparation with generative AI."  
    st.markdown(  
        "<style>#MainKenu{visibility:hidden;}</style>",  
        unsafe_allow_html=True  
    )  
    ##########st.image(im, width=650)  
    st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Poc</font></span>""", unsafe_allow_html=True)  
    st.markdown("""\n""")  
    st.markdown("Welcome to AI Interviewer! O AI Interviever is your personal interviewer powered"
                "by generative AI "  
                "that conducts mock interviews. You can upload your resume and AI"  )
    