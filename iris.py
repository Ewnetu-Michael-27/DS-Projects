import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


df_iris = sns.load_dataset("iris")

st.write("""
# Iris Dataset
How are Sepal_length and Petal_width correlate in among different species?
""")
Fig=px.scatter_3d(df_iris, x="sepal_length",y="petal_width",z="petal_length",color="species")
st.plotly_chart(Fig)
