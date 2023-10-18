import streamlit as st
import seaborn as sns
import altair as alt
from altair import datum
import pandas as pd
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Intro CAD and The Heart Dataset",
)

image=Image.open("heart.jpg")
st.image(image)

col=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]
df_heart=pd.read_csv("df_heart_clean_2.csv")

col_1=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"]
df_heart_mi=pd.read_csv("processed.cleveland.data", names=col_1)

st.title("Predicting The Presence of Coronary Artery Disease (CAD)")

st.write("Coronary artery disease (CAD) is caused by plaque buildup in the wall of the arteries that supply blood to the heart. Accoring to CDC, it is the most common type of heart disease in the US, killing 375,476 people in 2021.")


st.write("The dataset that was generated to study discriminant function models for estimating probabilities of coronary artery disease from clinical and non-invasive test results of 303 patients from Cleveland Clinic in Cleveland, Ohio. Concretely, the dataset explores the relationship between 13 clinical and non-invasive tests and the presence of CAD for the goal of building a prediction model.")

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
    st.write("Sex of the Individual: 1 for Male and 0 for Female")
elif option=="cp":
    st.write("Chest Pain Types. 1:ypical Angina, 2: Atypical Angina, 3: Non-Anginal Pain, 4: asymptomatic")
elif option=="trestbps":
    st.write("Resting Blood Pressure in mm of Hg at the admission to Hospital")
elif option=="chol":
    st.write("Serum Cholestrol in mg/dl")
elif option=="fbs":
    st.write("Fasting Blood Sugar >120 mg/dl. 1: True, 0:False")
elif option=="restecg":
    st.write("Resting Electrocardiographic Results. 0:Normal, 1:Having ST-T wave abnormality, 2:showing probable or definite left ventricular hypertrophy")
elif option=="thalach":
    st.write("maximum Heart Rate Achieved")
elif option=="exang":
    st.write("Exercise Induced Angina. 1:Yes, 0:NO")
elif option=="oldpeak":
    st.write("ST Depression Induced by excercise relative to rest")
elif option=="slope":
    st.write("The Slope of the peak exercise ST segment. 1: upsloping, 2: Flat, 3: Down sloping")
elif option=="ca":
    st.write("Number of major vessels colored by fluroscopy")
elif option=="thal":
    st.write("Thallium scintigraphy. 3: Normal, 6: Fixed Defect, 7: Reversable Defect")
elif option=="num":
    st.write("Diagnosis of Heart Disease (Angiographic Disease Status)")

st.text("")
st.markdown("***")

st.write("**About The Dataset**")
st.write("The data is relatively clean: only 6 missing values in 303 rows; only 2 columns affected. Moreover, the missigness seems MAR. KNN imputation is used to fix the missigness")
tab_a,tab_b=st.tabs(["The dataset before imputation","The dataset after imputation"])
with tab_a:
    fig=plt.figure(figsize=(20,4))
    sns.heatmap(df_heart_mi.eq('?').transpose(), cmap="crest").set(title='Missing Values')
    st.pyplot(fig)
with tab_b:
    fig=plt.figure(figsize=(20,4))
    sns.heatmap(df_heart.eq('?').transpose(), cmap="crest").set(title='Missing Values')
    st.pyplot(fig)


st.text("")
st.markdown("***")

st.write("In this dataset, 'num' is the target variable that shows the presence of CAD: 0 for absence (<50% diameter narrowing) and 1 for presence (>50% diameter narrowing). (See explanation below)")
pd_plot=pd.crosstab(df_heart["num"], df_heart["num"]).plot(kind='bar')
st.pyplot(pd_plot.figure)
with st.expander("See explanation"):
    st.write("The target is balanced. Roughly equal number of values for presence and absence.")


st.text("")
st.markdown("***")

st.write("Out of the 13 clinical and non-invasive tests (Features), 8 of them are categorical variables. Below, let's see their relationship with the presence of CAD (num)")

option1=st.selectbox(
    "Pick a categorical variable to see its relatioship with num (See explanation below for each feature)",
    ("sex", "cp", "fbs", "restecg","exang", "slope", "ca", "thal")
)
pd_plot=pd.crosstab(df_heart[option1], df_heart["num"]).plot(kind='bar')
st.pyplot(pd_plot.figure)
with st.expander("See explanation"):
    if option1=="sex":
        st.write("The data is not balanced in terms of sex: more male than female. Makes it difficult to analyze presence of CAD interms of sex")
    elif option1=="cp":
        st.write("Chest Pain of value 4 means asymptomatic. However, it is related with the most count of presence of CAD")
    elif option1=="fbs":
        st.write("Fasting Blood Sugar feature is imbalanced also it does not help in discerning presence of CAD")
    elif option1=="restecg":
        st.write("Increasing value of restecg very slightly correlates with the presence of CAD")
    elif option1=="exang":
        st.write("")
    elif option1=="slope":
        st.write("The Slope of the peak exercise ST segment")
    elif option1=="ca":
        st.write("Number of major vessels colored by fluroscopy")
    elif option1=="thal":
        st.write("Thallium scintigraphy")
            

st.text("")
st.markdown("***")

st.write("The rest 5 Features are continous variables. Below, let's see their relationship with the presence of CAD (num)")

option2=st.selectbox(
    "Pick a continious variable to see its relatioship with num (See explanation below)",
    ("age", "trestbps", "chol", "thalach", "oldpeak")
)

chart_alt=alt.Chart(df_heart).mark_boxplot().encode(
alt.Y(option2, type='quantitative').scale(zero=True),
alt.X('num:N', type='nominal'),
color=alt.Color('num:N')).properties(width=600).interactive()

st.altair_chart(chart_alt)
with st.expander("See explanation"):
     if option2=="age":
         st.write("age")
     elif option2=="trestbps":
         st.write("trestbps")
     elif option2=="chol":
         st.write("chol")
     elif option2=="thalach":
         st.write("thalach")
     elif option2=="oldpeak":
         st.write("oldpeak")
    

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

st.write("Level of Cholestrol (Chol), Resting Blood Pressure (Trestbps), Fasting Blood Sugar (FBS), Resting Electrocardiographic Results (Restecg), and The Slope of the peak excercise ST segment (Slope) are not a good indicators for the presence of CAD in of themselves. Hence, both output of the target, 0 and 1, are maped to the same values of the features")

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


