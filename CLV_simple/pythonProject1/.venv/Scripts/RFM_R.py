import pandas as pd
import numpy as np

df_order= pd.read_csv('../Lib/site-packages/orders.txt', sep='\t', encoding ="ISO-8859-1", parse_dates=['orderdate'])
df_customer=pd.read_csv('D:\DT\DQ\CRM_coop\data\customer.txt',sep='\t',encoding = "ISO-8859-1")
#print(df_order.dtypes)

df_order=df_order[['orderid','customerid','orderdate','totalprice']]

df=df_order.merge(df_customer[['customerid','householdid']],left_on='customerid',right_on='customerid')
#print(df.groupby('householdid').agg({'orderid':lambda x:len(x)}))
df_1=df.groupby('householdid').orderdate.max().reset_index()
df_1.columns=[['householdid','max_date']]
df_1['recency']=(df_1['max_date'].max()-df_1['max_date']).apply(lambda x:x.dt.days)
#print(df_1)

import matplotlib.pyplot as plt


'''plt.hist(df_1['recency'])
plt.show()


sse={}
from sklearn.cluster import KMeans
for n in range(1,10):
    kmeans=KMeans(n_clusters=n,random_state=0).fit(df_1['recency'].to_numpy())
    df_1['cluster']=kmeans.labels_
    sse[n]=kmeans.inertia_
    print(sse[n])
#print(df_1)
#print(sse.items())
plt.plot(sse.keys(),sse.values())
plt.show()'''

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=0).fit(df_1['recency'].to_numpy())
df_1['recency_cluster']=kmeans.predict(df_1['recency'].to_numpy())


df_1.columns=df_1.columns.get_level_values(0)
print(df_max.columns)
#function for ordering cluster number

def order_cluster(cluster_field_name,target_field_name,df,ascending):
    #new_cluster_field_name='new_'+cluster_field_name

    df_new=df.groupby(cluster_field_name)[target_field_name].meaan().reset_index()
    print(df_new)
    df_new=df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
    df_new['index']=df_new.index
    print(df_new)
    df_final=pd.merge(df,df_new[[cluster_field_name,'index']],on=cluster_field_name)
    print(df_final)
    df_final=df_final.drop([cluster_field_name],axis=1)
    df_final=df_final.rename(columns={"index":cluster_field_name})
    return df_final
df_ordered_by recency=order_cluster('recency_cluster','recency',df_1,False)
print(df_1)
