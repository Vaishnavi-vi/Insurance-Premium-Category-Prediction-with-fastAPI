from fastapi import FastAPI
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Literal,Annotated
import pickle
import pandas as pd

#import model 
with open("model.pkl","rb") as f:
    model=pickle.load(f)
    
    
#create a fast api app
app=FastAPI()

@app.get("/about")
def view():
    return {"message":"This is about predicting insurance premium"}

tier_city_1=["Chennai","Mumbai","Hyderabad","Delhi","Pune","Chandigarh","Kolkata","Banglore"]
tier_city_2=["Jaipur","Indore","Kota","Lucknow","Gaya","Jalandar","Mysore"]
#create a pydantic data for data validation
class user_input(BaseModel):
    age:Annotated[int,Field(...,description="Age of user",gt=0,lt=100)]
    weight:Annotated[float,Field(...,description="Weight of user",gt=0)]
    height:Annotated[float,Field(...,description="Height of user",gt=0)]
    income_lpa:Annotated[float,Field(...,description="Income of user in lpa",gt=0)]
    smoker:Annotated[bool,Field(...,description="is user a smoker")]
    city:Annotated[str,Field(...,description="city of user")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Occupation of the user")]
    
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def lifestyle_risk(self)->str:
            if self.smoker and self.bmi>30:
                return "high"
            elif self.smoker or self.bmi>27:
                return "medium"
            else:
                return "low"
    
    @computed_field
    @property
    def age_category(self)->str:
        if self.age<=18:
            return "Young"
        elif 18 < self.age <= 35:
            return "adult"
        elif 35 < self.age <= 50:
            return "middle-aged"
        else:
            return "senior-citizen"

        
    @computed_field
    @property
    def tier_city(self)->float:
        if self.city in tier_city_1:
            return 1
        elif self.city in tier_city_2:
            return 0
        
@app.post("/predict")
def predict_premium(data:user_input):
    
    input_df=pd.DataFrame([{"bmi":data.bmi,
                  "age_category":data.age_category,
                  "lifestyle_risk":data.lifestyle_risk,
                  "tier_city":data.tier_city,
                  "income_lpa":data.income_lpa,
                  "occupation":data.occupation}])
    
    prediction=model.predict(input_df)[0]
    
    return JSONResponse(status_code=201,content={"predicted_category":f"{prediction}"})



    
        
    
    
        
    
        