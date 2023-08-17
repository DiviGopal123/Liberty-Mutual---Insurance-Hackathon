import pandas as pd
import numpy as np
import seaborn as sns
import warnings
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle
warnings.filterwarnings("ignore")

df = pd.read_csv('Vehicle_Insurance_Data.csv')

df=df.drop(columns=['Customer_ID'])
df = pd.get_dummies(df,drop_first = True)

X = df.drop('Churn_Yes',axis=1)
y = df['Churn_Yes']

X_res, y_res = SMOTE().fit_resample(X,y)

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.3, random_state=47)

rf = RandomForestClassifier()
rf.fit(X_train,y_train)

pickle.dump(rf,open('churn_model_Updated_rf.pkl','wb'))
model=pickle.load(open('churn_model_Updated_rf.pkl','rb'))