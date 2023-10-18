import streamlit as st
import seaborn as sns
import altair as alt
from altair import datum
import pandas as pd
import plotly.express as px
from PIL import Image


st.set_page_config(
    page_title="Intro CAD and The Heart Dataset",
)

image=Image.open("heart.jpg")
st.image(image)

col=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]
df_heart=pd.read_csv("df_heart_clean_2.csv")


st.title("Predicting The Presence of Coronary Artery Disease (CAD)")

st.write("Coronary artery disease (CAD) is caused by plaque buildup in the wall of the arteries that supply blood to the heart. Accoring to CDC, it is the most common type of heart disease in the US, killing 375,476 people in 2021.")

st.write("The following dataset explores the relationship between 13 clinical and non-invasive tests and the presence of CAD for the goal of building a prediction model.")

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

st.write("In this dataset, 'num' is the target variable that shows the presence of CAD: 0 for absence and 1 for presence. (See explanation below image)")
pd_plot=pd.crosstab(df_heart["num"], df_heart["num"]).plot(kind='bar')
st.pyplot(pd_plot.figure)
with st.expander("See explanation"):
    st.write("The target is balanced. Roughly equal number of values for presence and absence.")


st.text("")
st.markdown("***")

st.write("Out of the 13 clinical and non-invasive tests (Features), 8 of them are categorical variables. Below, let's see their relationship with the presence of CAD (num)")

option1=st.selectbox(
    "Pick a categorical variable to see its relatioship with num (See explanation below image)",
    ("sex", "cp", "fbs", "restecg","exang", "slope", "ca", "thal")
)
pd_plot=pd.crosstab(df_heart[option1], df_heart["num"]).plot(kind='bar')
st.pyplot(pd_plot.figure)
with st.expander("See explanation"):
    st.write("Text will be added")
             

st.text("")
st.markdown("***")

st.write("The rest 5 Features are continous variables. Below, let's see their relationship with the presence of CAD (num)")

option2=st.selectbox(
    "Pick a continious variable to see its relatioship with num (See explanation below image)",
    ("age", "trestbps", "chol", "thalach", "oldpeak")
)

chart_alt=alt.Chart(df_heart).mark_boxplot().encode(
alt.Y(option2, type='quantitative').scale(zero=True),
alt.X('num:N', type='nominal'),
color=alt.Color('num:N')).properties(width=600).interactive()

st.altair_chart(chart_alt)
with st.expander("See explanation"):
    st.write("Text will be added")

st.text("")
st.markdown("***")

st.write("In any age group, achieving higer heart rate (Thalach) and minimizing excersie induced ST Depression (Oldpeak) is related to absence of CAD:0")


fig = px.parallel_coordinates(df_heart[["age","thalach","oldpeak","num"]], color="num", 
                              labels={"num": "Num",
                "age": "Age", "thalach": "Thalach",
                "oldpeak": "Oldpeak",},
                             color_continuous_scale=px.colors.diverging.Tealrose)
                             #color_continuous_midpoint=2)
st.plotly_chart(fig)
with st.expander("See explanation"):
    st.write("Select portion of the 'num' axis around 0 to see the relationship")

st.text("")
st.markdown("***")

st.write("Level of Cholestrol (Chol), Resting Blood Pressure (Trestbps), Fasting Blood Sugar (FBS), Resting Electrocardiographic Results (Restecg), and The Slope of the peak excercise ST segment (Slope) are not a good indicators for the presence of CAD in of themselves. Hence, both output of the target, 0 and 1, are maped to the same values")

option3=st.selectbox(
    "Add text",
    ("chol", "trestbps","fbs", "restecg","slope")
)


temp_array=[option3]
temp_array.append("num")

fig_2 = px.parallel_coordinates(df_heart[temp_array], color="num", 
                              labels={"num": "Num",
                "chol": "Cholestrol Level","slope":"Slope of PE-ST-S"},
                             color_continuous_scale=px.colors.diverging.Tealrose,
                               width=600,height=600)
                             #color_continuous_midpoint=2)
st.plotly_chart(fig_2)


