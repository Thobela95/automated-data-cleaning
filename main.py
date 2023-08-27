import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd
import pandas_profiling

from streamlit_pandas_profiling import st_profile_report

from Dora import Dora

from AutoClean import AutoClean

# # 1. as sidebar menu
# with st.sidebar:
#     selected = option_menu("Main Menu", ["Home", 'Settings'], 
#         icons=['house', 'gear'], menu_icon="cast", default_index=1)
#     selected

# 2. horizontal menu
selected2 = option_menu("Skoonmaker", ["Home", "Upload","Profiling" ,"Automatic Data Cleaning"], 
    icons=['house', 'cloud-upload', "zoom-in","ui-checks-grid"], 
    menu_icon="filter-circle-fill", default_index=0, orientation="horizontal")
# selected2
if selected2 == 'Home':
    st.write('Home')
    image = Image.open("workflow.jpg")
    st.image(image, caption ='Automated Data Cleaning Workflow')

if selected2 == 'Upload':
    st.title('Upload your data here')
    uploaded_file = st.file_uploader("Choose a file",type=['csv','xlsx','txt','pkl','dta','sav'])
    if uploaded_file is not None:
        if uploaded_file.name.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.lower().endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        elif uploaded_file.name.lower().endswith('.txt'):
            df = pd.read_fwf(uploaded_file)
        elif uploaded_file.name.lower().endswith('.pkl'):
            df = pd.read_pickle(uploaded_file)
        elif uploaded_file.name.lower().endswith('.dta'):
            df = pd.read_stata(uploaded_file)
        elif uploaded_file.name.lower().endswith('.sav'):
            df = pd.read_spss(uploaded_file.read())
        st.session_state['df']=df

if selected2 == 'Profiling':
    df = st.session_state['df']
    if df is not None:
        pr = df.profile_report()
        st_profile_report(pr)
    else:
        st.write("No data was found! Load Data to generate a profile report")

if selected2 == 'Automatic Data Cleaning':
    df = st.session_state['df']
    if df is not None:
        pipeline = AutoClean(df)
        st.write(pipeline.output)
        df = pipeline.output
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
            
        csv = convert_df(df)
        st.download_button(
            "Press to Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )
    else:
        st.write("No data was found! Load Data to perform automated data cleaning")
        

