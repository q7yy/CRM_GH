import pandas as pd
import numpy as np
import seaborn as  sns
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
df_model= pd.read_csv('../Lib/site-packages/ds_model_36mo.csv', sep=',')
df_pred= pd.read_csv('../Lib/site-packages/ds_pred_12mo.csv', sep=',')
df_model=df_model[['householdid', 'recency', 'monetary', 'frequency','clv']]
df_model['churned']=df_model['clv'].apply(lambda x:True if np.isnan(x) else False)
#print(df_model)
'''ax=sns.countplot(x='churned',data=df_model)
plt.show()
#imbalaced dataset:1.data based 2. model based'''
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression



# for rs in range(0,100):
clf=DecisionTreeClassifier(random_state=0).fit(df_model[['recency', 'monetary', 'frequency']],df_model['churned'])
y_churned=clf.predict(df_pred[['recency', 'monetary', 'frequency']])
df_pred['pred_churned']=y_churned
#print(df_pred['pred_churned'].value_counts())

df_pred_churned=df_pred[df_pred['pred_churned']==True]
df_pred_returned=df_pred[df_pred['pred_churned']==False]

df_model=df_model[df_model['churned']==False]
x_train,x_test,y_train,y_test=train_test_split(df_model[['recency', 'monetary', 'frequency']]
                                               ,df_model[['clv']],test_size=0.33,random_state=42)
from sklearn.linear_model import LinearRegression
reg=LinearRegression().fit(x_train,y_train)
y_pred=reg.predict(x_test)
df_result=y_test.copy()
df_result['pred_clv']=y_pred
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
print(df_result.shape)
print(f"Linear regression MAE:{mean_absolute_error(df_result['pred_clv'],df_result['clv'])}")
print(f"Linear regression MSE {mean_squared_error(df_result['pred_clv'],df_result['clv'])}")

from sklearn.tree import DecisionTreeRegressor
reg=DecisionTreeRegressor(random_state=0).fit(x_train,y_train)
y_pred=reg.predict(x_test)
df_result=y_test.copy()
df_result['pred_clv']=y_pred
print(f"Decision Tree MAE:{mean_absolute_error(df_result['pred_clv'],df_result['clv'])}")
print(f"Decision Tree MSE {mean_squared_error(df_result['pred_clv'],df_result['clv'])}")

x_train,x_test,y_train,y_test=train_test_split(df_model[['recency', 'monetary', 'frequency']]
                                               ,df_model['clv'],test_size=0.33,random_state=42)
from sklearn.ensemble import RandomForestRegressor
reg=RandomForestRegressor(random_state=0,n_estimators=1000).fit(x_train,y_train)
y_pred=reg.predict(x_test)
df_result=y_test.to_frame(name='clv')
df_result['pred_clv']=y_pred
print(f"RandomForestRegressor MAE:{mean_absolute_error(df_result['pred_clv'],df_result['clv'])}")
print(f"RandomForestRegressor MSE {mean_squared_error(df_result['pred_clv'],df_result['clv'])}")

