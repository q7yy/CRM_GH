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
x_train,x_test,y_train,y_test=train_test_split(df_model[['recency', 'monetary', 'frequency']]
                                               ,df_model['churned'],test_size=0.33,random_state=42)


# for rs in range(0,100):
clf=DecisionTreeClassifier(random_state=0).fit(x_train,y_train)
y_churned=clf.predict(df_pred[['recency', 'monetary', 'frequency']])
df_pred['pred_churned']=y_churned
print(df_pred['pred_churned'].value_counts())