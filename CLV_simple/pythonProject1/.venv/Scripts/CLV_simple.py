import pandas as pd
import numpy as np

df = pd.read_csv('../Lib/site-packages/orders.txt', sep='\t', encoding ="ISO-8859-1", parse_dates=['orderdate'])
print(df)
print(df.columns)
print(df.dtypes)

margin=0.05
AC=1

#LTV=margin*avg_order#freq/churn-AC

customers=df.groupby('customerid').agg({"orderdate": lambda x:(x.max()-x.min()).days,
                                        "totalprice":lambda x: x.sum(),
                                        "orderid":lambda x: len(x)})
print(customers)
retention=customers[customers['orderid']>1].shape[0]/customers.shape[0]
print(customers[customers['orderid']>1])
print(customers.shape[0])
customers=customers[customers['orderdate']>0]

avg_order=customers['totalprice'].sum()/customers['orderid'].sum()
freq= customers['orderid'].sum()/customers['orderdate'].sum()
print(customers)
print(f' avg_order:{avg_order} and freq:{freq}')
print(margin*avg_order*freq/(1-retention)-AC)