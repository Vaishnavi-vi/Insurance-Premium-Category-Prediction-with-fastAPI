import streamlit as st
import requests
from PIL import Image

API_URL="http://localhost:8000/predict"

st.set_page_config("Predict Insurance Premium",layout="wide")
page=st.sidebar.radio("Go to",["Intro","Predict Insurance Premium"])
if page=="Intro":
    st.title("Predict Insurance Premium")
    image=Image.open("C:\\Users\\Dell\\Downloads\\insurance.img")
    st.image(image,use_container_width=True)
elif page=="Predict Insurance Premium":
    st.title("Insurance Premium Category Prediction")

    st.header("Enter your details here")

#Input Fields
    age = st.number_input("Age", min_value=16, max_value=120, step=1)

    weight = st.number_input("Weight (kg)", min_value=12.0, step=0.5)

    height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, step=0.01)

    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.0, step=0.1)
    smoker=st.selectbox("Are you Smoker",["Select one",True,False])
    city=st.selectbox("From which city tou belong",['Select one','Jaipur', 'Chennai', 'Indore', 'Mumbai', 'Kota', 'Hyderabad',
       'Delhi', 'Chandigarh', 'Pune', 'Kolkata', 'Lucknow', 'Gaya',
       'Jalandhar', 'Mysore', 'Banglore'])
    occupation=st.selectbox("What is your Occupation:",["Select one",'retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'])

    if st.button("Predict Premium category"):
        input_data={
        "age":age,
        "weight":weight,
        "height":height,
        "income_lpa":income_lpa,
        "smoker":smoker,
        "city":city,
        "occupation":occupation
        } 
    
        try:
            response=requests.post(API_URL,json=input_data)
            if response.status_code in [200,201,202]:
                result=response.json()
                st.success(f"Predicted Insurance Premium Category: **{result['predicted_category']}** ")
            else:
                st.warning(f"API Error:{response.status_code}-{response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to fast Api server")
                       
            
    
