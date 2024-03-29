# -*- coding: utf-8 -*-
"""Demand Forecasting -  Big Mart Sales Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UVCog0KtKpSizOREnqnLICa_vYO241WR

### Case Study: Big Mart Sales Prediction


**importing the dependencies**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

"""data collection and analysis

"""

big_mart_data = pd.read_csv('/content/Train.csv')

#first five rows of dataframe
big_mart_data.head()

#no. of rows and columns i.e, products and features
big_mart_data.shape

#getting some informations about the dataset
big_mart_data.info()

"""**Categorical Features:**
- Item_Identifier
- Item_Fat_Content
- Item_Type
- Outlet_Identifier
- Outlet_Size
- Outlet_Location_Type
- Outlet_Type
"""

#checking missing values
big_mart_data.isnull().sum()

"""Handling Missing values (imputation)


"""

#mean value of item weight column
big_mart_data['Item_Weight'].mean()

#filling missing values in item weight column with mean value
big_mart_data['Item_Weight'].fillna(big_mart_data['Item_Weight'].mean(), inplace=True)

#checking if its updated
big_mart_data.isnull().sum()

"""**Replacing the missing values in outlet size column with mode **


(The missing values in the "outlet size" column will be filled by the mode since the data is categorical)
"""

big_mart_data['Outlet_Size'].mode()

mode_of_Outlet_size = big_mart_data.pivot_table(values='Outlet_Size', columns='Outlet_Type', aggfunc=(lambda x: x.mode()[0]))

print(mode_of_Outlet_size)

missing_values = big_mart_data['Outlet_Size'].isnull()

missing_values

big_mart_data.loc[missing_values, 'Outlet_Size'] = big_mart_data.loc[missing_values,'Outlet_Type'].apply(lambda x: mode_of_Outlet_size[x])

big_mart_data.isnull().sum()

"""# Data Analysis"""

#statistical measures about the data
big_mart_data.describe()

"""**Numerical Features**"""

sns.set()

#item weight colum distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Weight'])
plt.show()

#item visibility colum distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Visibility'])
plt.show()

#item mrp colum distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_MRP'])
plt.show()

#item Item_Outlet_Sales colum distribution
plt.figure(figsize=(6,6))
sns.distplot(big_mart_data['Item_Outlet_Sales'])
plt.show()

#item output establishment year colum distribution
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Establishment_Year', data=big_mart_data)
plt.show()

"""**Categorical Features**"""

# Item_Fat_Content column
plt.figure(figsize=(6,6))
sns.countplot(x='Item_Fat_Content', data=big_mart_data)
plt.show()

# Item_Type column
plt.figure(figsize=(30,6))
sns.countplot(x='Item_Type', data=big_mart_data)
plt.show()

# Outlet_Size column
plt.figure(figsize=(6,6))
sns.countplot(x='Outlet_Size', data= big_mart_data)
plt.show()

"""**Data Pre-Processing**"""

big_mart_data.head()

big_mart_data['Item_Fat_Content'].value_counts()

big_mart_data.replace({'Item_Fat_Content': {'low fat':'Low Fat','LF':'Low Fat', 'reg':'Regular'}}, inplace=True)

big_mart_data['Item_Fat_Content'].value_counts()

"""**Label Encoding**

convert categorical values and transform them into numerical value
"""

encoder = LabelEncoder()

big_mart_data['Item_Identifier'] = encoder.fit_transform(big_mart_data['Item_Identifier'])

big_mart_data['Item_Fat_Content'] = encoder.fit_transform(big_mart_data['Item_Fat_Content'])

big_mart_data['Item_Type'] = encoder.fit_transform(big_mart_data['Item_Type'])

big_mart_data['Outlet_Identifier'] = encoder.fit_transform(big_mart_data['Outlet_Identifier'])

big_mart_data['Outlet_Size'] = encoder.fit_transform(big_mart_data['Outlet_Size'])

big_mart_data['Outlet_Location_Type'] = encoder.fit_transform(big_mart_data['Outlet_Location_Type'])

big_mart_data['Outlet_Type'] = encoder.fit_transform(big_mart_data['Outlet_Type'])

big_mart_data.head()

"""**Splitting features and Target**"""

X = big_mart_data.drop(columns='Item_Outlet_Sales', axis=1)
Y = big_mart_data['Item_Outlet_Sales']

X

Y

"""**Splitting the data into Training data & Testing Data**"""

X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size=0.2,random_state=2)

print(X.shape, X_train.shape, X_test.shape)

"""**Machine Learning Model Training**

XGBoostRegressor
"""

regressor = XGBRegressor()

regressor.fit(X_train,Y_train)

"""**Evaluation**"""

#Prediction on test data
test_data_prediction = regressor.predict(X_test)

#r squared value
r2_test = metrics.r2_score(Y_test, test_data_prediction)

print('R Squared value = ', r2_test)

# Calculate Mean Absolute Error (MAE)
mae = metrics.mean_absolute_error(Y_test, test_data_prediction)
print('Mean Absolute Error (MAE) = ', mae)

# Calculate Root Mean Squared Error (RMSE)
rmse = np.sqrt(metrics.mean_squared_error(Y_test, test_data_prediction))
print('Root Mean Squared Error (RMSE) = ', rmse)
