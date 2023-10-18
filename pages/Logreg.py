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
import numpy as np

st.set_page_config(
    page_title="Logreg on The Heart Dataset",
)
st.title("Further Analysis on The Clinical Features and CAD")

#col=["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]

X=pd.read_csv("X.csv", index_col=False)
y=pd.read_csv("y.csv", index_col=False)

#to pass to the training model
x_1=X[["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]]


st.write("To further analyze the relationship between the clinical features and CAD, P-value analysis from Logit Model is utilised. P-value less than 0.05 suggest a stastically significant relationship between the feature and the target.")

st.text("")
st.markdown("***")


st.write("Below, P-values for each feature are shown. The points are red for those feature with P-value >0.05")


logit_model=sm.Logit(y["num"],X)
result_1=logit_model.fit()
p_values=[]
    
for i in result_1.pvalues:
    p_values.append(i)
    
col=X.columns 
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
with st.expander("See explanation"):
    st.write("Text will be added")

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

    z = np.flip(confusion_matrix_1,0)
    x = ['Predict 1', 'Prdict 0']
    y =  ['True 0', 'True 1']

    # change each element of z to type string for annotations
    z_text = [[str(x) for x in y] for y in z]

    # set up figure 
    fig = ff.create_annotated_heatmap(z, y=y, x=x, annotation_text=z_text, colorscale='Viridis')

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
        




