import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from flask import Flask, request, render_template, send_file
import pickle
import re
import math
from imblearn.over_sampling import SMOTE
import joblib
from io import BytesIO
import os

app = Flask("__name__")

model=pickle.load(open('churn_model_Updated_rf.pkl','rb'))

@app.route("/")
def loadPage():
	return render_template('index.html')

@app.route("/home")
def loadHomePage():
	return render_template('home.html')

@app.route("/excelupload")
def loadUploadPage():
	return render_template('excelupload.html')

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    print("Inside /download")
    try:
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404
@app.route('/Vehicle_Insurance_Data_Template.csv')
def download_excel():
    filename='templates/Vehicle_Insurance_Data_Template.csv'
    return send_file(filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():
    print("Inside upload")
    if 'csv_file' not in request.files:
        return "No file part"

    csv_file = request.files['csv_file']
    print("Read the csv file")
    
    # Load the uploaded CSV file into a pandas DataFrame
    df_org = pd.read_csv(csv_file)
    
    df_new = df_org.copy()
    df_new = df_new.drop(columns=['Customer_ID'])
    
    print("Skipped first row & Dropped Customer ID successfully")
    
    df_new = pd.get_dummies(df_new,drop_first = True)
    print("converted to binary data")
    
    pred = model.predict(df_new)
    
    # Mapping of values to text labels
    label_mapping = {
        0: "No",
        1: "Yes"
        }
    
    # Convert predicted values to text labels
    predicted_labels = [label_mapping[value] for value in pred]
    
    df_org['Churn_Prediction']=predicted_labels
    
    # Create a new CSV file with the prediction results
    result_csv = BytesIO()
    
    df_org.to_csv(result_csv,index=False)
    result_csv.seek(0)
    
    # Save the result CSV to a temporary file
    temp_filename = 'result.csv'
    df_org.to_csv(temp_filename, index=False)

    # Send the result file to the user as a downloadable file
    result_file_url = f'/download/{temp_filename}'
    print("result_file_url", result_file_url)
    return render_template('excelupload.html', result_file_url=result_file_url)

    # Send the result file to the user as a downloadable file
    #return send_file(
    #    result_csv,
    #    mimetype='text/csv',
    #    as_attachment=True,
    #    attachment_filename='prediction_result.csv'
    #)

@app.route("/predict", methods=['POST'])
def predict():
    print("button clicked")
    customerId = int(request.form['customer_id'])
    
    inputQuery1 = request.form['Monthly_Premium']
    inputQuery2 = request.form['open_policies']
    inputQuery3 = request.form['Renew_Offer_Type']
    inputQuery4 = request.form['Vehicle_Age_In_Years']
    inputQuery5 = request.form['weeks_since_claim']
     
    city = request.form['city']
    inputQuery8= 1 if city=='Indianapolis' else 0
    inputQuery9= 1 if city=='Tampa' else 0
    inputQuery7= 1 if city=='Fairfield' else 0
    #inputQuery10= 1 if city=='Boston' else 0
    inputQuery6= 1 if city=='Denver' else 0
    
    work_status = request.form['work_status']
    inputQuery10 = 1 if work_status=='employed' else 0
    inputQuery11 = 1 if work_status=='medical_leave' else 0
    inputQuery12 = 1 if work_status=='retired' else 0
    inputQuery13 = 1 if work_status=='unemployed' else 0
    #inputQuery14 = 1 if work_status=='disabled' else 0
    
    gender=request.form['gender']
    inputQuery14= 1 if gender=='male' else 0
    #inputQuery5= 1 if gender=='female' else 0

    premium_type = request.form['Coverage_Type']
    inputQuery15= 1 if premium_type=='premium_plan' else 0
    inputQuery16= 1 if premium_type=='primary_plan' else 0
    #inputQuery16= 1 if premium_type=='Extended_Plan' else 0
  
   
    accessbility = request.form['Accessbility']

    inputQuery17 = 1 if accessbility =='customer_call' else 0
    inputQuery18 = 1 if accessbility =='Direct_Branch_Contact' else 0
    inputQuery19 = 1 if accessbility =='Website' else 0
    #inputQuery19 = 1 if reachability =='agents' else 0
    
    typeCar =  request.form['type_of_vehicle']
    inputQuery20 = 1 if typeCar == 'Luxirious_Car' else 0
    inputQuery21 = 1 if typeCar == 'Luxurious_SUV' else 0
    inputQuery22 = 1 if typeCar == 'SUV' else 0
    inputQuery23 = 1 if typeCar == 'Sedan_4 Door' else 0
    inputQuery24 = 1 if typeCar == 'Sports_Car' else 0
    #inputQuery24 = 1 if typeCar == 'Coupe_2 Door' else 0
    #int_features=[int(x) for x in request.form.values()]
    #features=[np.array(int_features)]
    prediction = model.predict([[inputQuery1,inputQuery2,inputQuery3,inputQuery4,inputQuery5,inputQuery6,inputQuery7,inputQuery8,inputQuery9,inputQuery10,inputQuery11,inputQuery12,inputQuery13,inputQuery14,inputQuery15,inputQuery16,inputQuery17,inputQuery18,inputQuery19,inputQuery20,inputQuery21,inputQuery22,inputQuery23,inputQuery24]])
    
    print(prediction)
    
    if prediction==1:
        output = "Customer %d will exit the company" % (customerId)
    else:
        output = "Customer %d will not exit the company" % (customerId)
    #, customer_id = request.form['customer_id'], payment_per_month = request.form['payment_per_month'], weeks_since_claim = request.form['weeks_since_claim'], open_policies = request.form['open_policies'], Renew_Offer_Type = request.form['Renew_Offer_Type'
    return render_template('home.html', output1=output)
    
app.run(debug=True)