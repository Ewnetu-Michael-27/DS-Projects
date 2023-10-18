import streamlit as st
import seaborn as sns
import altair as alt
from altair import datum
import pandas as pd
import plotly.express as px



col=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]
df_heart=pd.read_csv("df_heart_clean_2.csv")


st.set_page_config(
    page_title="Intro CAD and The Heart Dataset",
)

st.title("Pridicting Presence of Coronary Artery Disease")

st.write("*Regarding prediction model, check second page on sidebar* :sunglasses:")


st.sidebar.success("Select a page above.")

st.text("")
st.markdown("***")

option=st.selectbox(
    "The variables are medical terminologies. Choose from below to see further discription about them",
    ("age","sex", "cp", "trestbps", "chol", 
     "fbs", "restecg", "thalach", 
     "exang", "oldpeak", "slope", "ca", "thal", "num")
)

if option=="age":
    st.write("Age of the Individual")
elif option=="sex":
    st.write("Sex of the Individual")
elif option=="cp":
    st.write("Chest Pain Types")
elif option=="trestbps":
    st.write("Resting Blood Pressure in mm of Hg at the admission to Hospital")
elif option=="chol":
    st.write("Serum Cholestrol in mg/dl")
elif option=="fbs":
    st.write("Fasting Blood Sugar")
elif option=="restecg":
    st.write("Resting Electrocardiographic Results")
elif option=="thalach":
    st.write("maximum Heart Rate Achieved")
elif option=="exang":
    st.write("Exercise Induced Angina")
elif option=="oldpeak":
    st.write("ST Depression Induced by excercise relative to rest")
elif option=="slope":
    st.write("The Slope of the peak exercise ST segment")
elif option=="ca":
    st.write("Number of major vessels colored by fluroscopy")
elif option=="thal":
    st.write("Thallium scintigraphy")
elif option=="num":
    st.write("Diagnosis of Heart Disease (Angiographic Disease Status)")

st.text("")
st.markdown("***")

option2=st.selectbox(
    "Pick a variable to see its relatioship with num",
    ("age","sex", "cp", "trestbps", "chol", 
     "fbs", "restecg", "thalach", 
     "exang", "oldpeak", "slope", "ca", "thal", "num")
)


#Continous variable
if option2 in ["oldpeak", "trestbps", "thalach", "age", "chol"]:
    chart_alt=alt.Chart(df_heart).mark_boxplot().encode(
    alt.Y(option2, type='quantitative').scale(zero=True),
    alt.X('num:N', type='nominal'),
    color=alt.Color('num:N')).properties(width=600).interactive()

    st.altair_chart(chart_alt)

#categorical variables
elif option2 in ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal", "num"]:
    pd_plot=pd.crosstab(df_heart[option2], df_heart["num"]).plot(kind='bar')
    st.pyplot(pd_plot.figure)
    #chart_alt_2=alt.Chart(df_heart).mark_boxplot().encode(
    #alt.Y(option2, type='nominal'),
    #alt.X('num:N', type='nominal'),
    #color='num:N').properties(width=600).interactive()

    #st.altair_chart(chart_alt_2)

st.text("")
st.markdown("***")

st.write("Parrllel plot of Age, Thalach, Oldpeak, num")

#x=st.button("Parallel Plot")

fig = px.parallel_coordinates(df_heart[["age","thalach","oldpeak","num"]], color="num", 
                              labels={"num": "Num",
                "age": "Age", "thalach": "Thalach",
                "oldpeak": "Oldpeak",},
                             color_continuous_scale=px.colors.diverging.Tealrose)
                             #color_continuous_midpoint=2)
st.plotly_chart(fig)

st.text("")
st.markdown("***")

fig_2 = px.parallel_coordinates(df_heart[["chol","num"]], color="num", 
                              labels={"num": "Num",
                "age": "Age", "thalach": "Thalach",
                "oldpeak": "Oldpeak",},
                             color_continuous_scale=px.colors.diverging.Tealrose,
                               width=600,height=600)
                             #color_continuous_midpoint=2)
st.plotly_chart(fig_2)


