import streamlit as st
import pandas as pd
import seaborn as sns 

#loading the data as dataframe
df_heart=pd.read_csv("processed.cleveland.data", names=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"])

st.write("# Deploying Streamlit on the Heart Dataset")
st.write("## Choose the following features")
col1, col2=st.columns([1,1])

col3, col4=st.columns([0.3,0.7])


thal=col1.checkbox("Thalach")
age=col2.checkbox("Age")

if thal:
    s1="thalach"

if age:
    s2="age"

if thal==True and age==True:
    with st.container():
        col3.markdown("Regplot between Thalach and Age")
        x=sns.regplot(x=s1, y=s2, data=df_heart, lowess=True)
        col4.pyplot(x.figure)
        "Thalach is maximum heart rate achieved"


