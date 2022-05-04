import streamlit as st
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, AdaBoostClassifier
import streamlit.components.v1 as components


html = """
  <style>
  u{
  text-decoration-line: underline;
  text-decoration-style: double;
  }

  mark{
  
  font-size:110%;
  color: black;

  }



  font{
   color: grey;
  }

  embed:focus {
  outline: none;
}
  border-radius:50%;
    
  </style>
"""




# crop Advisory for Farmers

st.markdown('<style>' + open('css/title.css').read() + '</style>', unsafe_allow_html=True)


st.markdown(html, unsafe_allow_html=True)
r1=pd.read_csv("Dataset/r1.csv")
crop_data=pd.read_csv("Dataset/crop_data.csv")
st.markdown('<div class="title">कृषि उपज मार्गदर्शक 🌾 </div>', unsafe_allow_html=True)

st.sidebar.write('<div class="subheader-sidebar">राज्य की पसंदगी :</div>',unsafe_allow_html=True)	
State_list=list(r1['state'].unique())
State=st.sidebar.selectbox("राज्य : ",r1['state'].unique())
attributes=[]


#rainfall prediction
st.write('<div class="subheader">Predicted rainfall in your state in 2020 :<br>[अनुमानित बारिश  वर्ष 2020 में] </div>',unsafe_allow_html=True)
x=pd.DataFrame(r1,columns=['le_state','le_year'])
y=pd.DataFrame(r1,columns=['rainfall_avg'])
lr=GradientBoostingRegressor(learning_rate=0.1,n_estimators=246,min_samples_leaf=80,random_state=40).fit(x,y)

if State:
	pred_data=[[State_list.index(State),120]]
	#rainfall prediction
	pred=lr.predict(pred_data)
	strr_=str(pred)
	strr_=strr_.replace('[[','')
	strr_=strr_.replace(']]','')

	st.write("<mark> %s mm</mark>" %strr_,unsafe_allow_html=True)
	st.sidebar.write('<div class="subheader-sidebar">पाक की विगत : </div>',unsafe_allow_html=True)	
	Season_list=list(crop_data['Season'].unique())
	Season=st.sidebar.selectbox("ऋतु : ",crop_data['Season'].unique())
	ph=st.sidebar.number_input("PH का मूल्य : ",0.5,8.5,0.5)
	n=st.sidebar.number_input("नाइट्रोजन का प्रमाण : ",2.0,90.0,2.0)
	p=st.sidebar.number_input("फोस्फरस का प्रमाण : ",1.0,50.0,1.0)
	k=st.sidebar.number_input("पोटेसियम का प्रमाण: ",0.5,20.0,0.5)
	# ph=st.sidebar.number_input("Enter PH content: ",0.5,8.5,0.5)
	# n=st.sidebar.number_input("Enter Nitrogen content: ",2.0,90.0,2.0)
	# p=st.sidebar.number_input("Enter Phosphorous content: ",1.0,50.0,1.0)
	# k=st.sidebar.number_input("Enter Potassium content: ",0.5,20.0,0.5)
	# temp=st.sidebar.number_input("Enter temperature: ",2.0,50.0,2.0)
	temp=st.sidebar.number_input("तापमान : ",2.0,50.0,2.0)
	st.write('<div class="subheader">Most profitable crop for you :<br> [सबसे फ़ायदेकिय फसल] </div>',unsafe_allow_html=True )

	x_=crop_data[['Season_le','ph_avg','n','p','k','avg_temp','rainfall_avg']]
	y_=crop_data.Crop
	clf=AdaBoostClassifier(learning_rate=0.146731,n_estimators=18,random_state=40).fit(x_,y_)
	i=Season_list.index(Season)
	predictors=[i,ph,n,p,k,temp,pred]
	str_=str(clf.predict([predictors]))
	#st.write(str(clf.predict([predictors])))
	str_=str_.replace('[\'','')
	str_=str_.replace('\']','')

	
	# st.subheader(str_)
	st.write("<mark>%s</mark>" % str_,unsafe_allow_html=True)

	

	if st.button("फसल की जानकारी"):
		if str_=="Arhar/Tur":
			st.image(r"D:\Crop-Advisory-for-Farmers-main\data_insights/Arhar_Tur.png", width=800)
		st.image(r"D:\Crop-Advisory-for-Farmers-main\data_insights/%s.png" % str_, width=800)

		


