import streamlit as st
import seaborn as sns
import altair as alt
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import math

st.set_page_config(
    page_title="Logreg on The Heart Dataset",
)
st.title("Further Analysis on Clinical Features and CAD")

#col=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]

X=pd.read_csv("X.csv", index_col=False)
y=pd.read_csv("y.csv", index_col=False)

#to pass to the training model
x_1=X[["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]]


st.write("Click here to utlize the Logit Model from Statsmodel and check the performance of each variables")

logit_model=sm.Logit(y["num"],X)
result_1=logit_model.fit()

col=X.columns
st.write("Here are the P values for the variables")
col=X.columns 
p_values=[]
    
for i in result_1.pvalues:
    p_values.append(i)

df_p_val=pd.DataFrame(list(zip(p_values, col)), columns=["P_values", "Variables"])
chart_1 = alt.Chart(df_p_val).mark_point().encode(
    x='Variables:N',
    y="P_values:Q",
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.P_values > 0.05,  
        alt.value('red'),     
        alt.value('blue')   
        ),
        tooltip=["Variables","P_values"]
    ).properties(width=600)
    #line = alt.Chart().mark_rule(color="red").encode(y=alt.datum(0.05),size=alt.value(5))
    #chart_main=line+chart_1

tab1, tab2, tab3=st.tabs(["P_values chart","Variables with P_value>0.05", "Variables with P_value<0.05"])
with tab1:
    st.altair_chart(chart_1,use_container_width=True)
with tab2:
    st.dataframe(df_p_val[df_p_val["P_values"]>0.05])
with tab3:
    st.dataframe(df_p_val[df_p_val["P_values"]<0.05])

st.text("")
st.markdown("***")

#recompute P values 

st.markdown("Pick Variables and run Logistic Regression Model (To increase accuracy, pick variables with P values <0.05)")

#button_2=st.button("Pick variables")

#list_p_val=[]


list_p_val=st.multiselect("Pick varaibles",
                              ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
                               "thalach", "exang", "oldpeak", "slope", "ca", "thal"] ,
                               ["age","sex","cp","thalach","exang","ca","thal"])
    
button_3=st.button("Click When Done Selecting")
if button_3:
    
    X_new=X[list_p_val]
    X_train, X_test, y_train, y_test = train_test_split(X_new, y["num"], test_size=0.3, random_state=0)
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)
    score=logreg.score(X_test, y_test)
    confusion_matrix_1 = confusion_matrix(y_test, y_pred)
    
    score_x=str(math.floor(score*100))+"%"
    st.metric("Accuracy over Test Samples",score_x)

    z = confusion_matrix_1
    x = ['Predict 0', 'Prdict 1']
    y =  ['True 1', 'True 0']

    # change each element of z to type string for annotations
    z_text = [[str(y) for y in x] for x in z]

    # set up figure 
    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis')

    # add title
    fig.update_layout(title_text='<i><b>Confusion matrix</b></i>',
                  #xaxis = dict(title='x'),
                  #yaxis = dict(title='x')
                 )

    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                        x=0.5,
                        y=-0.15,
                        showarrow=False,
                        text="Predicted value",
                        xref="paper",
                        yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                        x=-0.35,
                        y=0.5,
                        showarrow=False,
                        text="Real value",
                        textangle=-90,
                        xref="paper",
                        yref="paper"))

    # adjust margins to make room for yaxis title
    fig.update_layout(margin=dict(t=50, l=200))

    # add colorbar
    fig['data'][0]['showscale'] = True
    st.plotly_chart(fig)
        




