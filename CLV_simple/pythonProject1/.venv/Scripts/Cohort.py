import pandas as pd
import numpy as np
df_order= pd.read_csv('../Lib/site-packages/orders.txt', sep='\t', encoding ="ISO-8859-1", parse_dates=['orderdate'])
df_customer=pd.read_csv('D:\DT\DQ\CRM_coop\data\customer.txt',sep='\t',encoding = "ISO-8859-1")
df_order=df_order[['orderid','customerid','orderdate','totalprice']]
df=df_order.merge(df_customer[['customerid','householdid']],left_on='customerid',right_on='customerid')
#check if there is missing value:print(df.isna().values.sum())
#Cohort month---order month
import datetime as dt
df['order_month']=df['orderdate'].apply(lambda x: dt.datetime(x.year,x.month,1))

df_g_h=df.groupby('householdid')['order_month'].min().reset_index()
df_g_h.columns=['householdid','cohort']
df=df.merge(df_g_h,left_on='householdid',right_on='householdid')
df['cohort_month']=df['orderdate'].apply(lambda x: x.year*12+x.month)-df['cohort'].apply(lambda x: x.year*12+x.month)+1
print(df)
df['cohort']=df['cohort'].dt.strftime('%Y/%m')
print(df)
df_cohort=df.groupby(['cohort','cohort_month'])['householdid'].apply(pd.Series.nunique).reset_index()
df_pivot=df_cohort.pivot(index='cohort',columns='cohort_month',values='householdid')
df_retention=df_pivot.divide(df_pivot.iloc[:,0],axis=0)
df_retention=df_retention.round(3)*100

#print(df_pivot)
print(df_retention)
#print(df)

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(18,10))
ax=sns.heatmap(df_retention.iloc[0:5,0:11],annot=True,vmin=0.0,vmax=10,cmap='YlGnBu',fmt='g')
plt.show()
print(df_retention.iloc[0:5,0:11])