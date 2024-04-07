import pandas as pd
import numpy as np
from datetime import timedelta
from dateutil.relativedelta import relativedelta
df_order= pd.read_csv('../Lib/site-packages/orders.txt', sep='\t', encoding ="ISO-8859-1", parse_dates=['orderdate'])
df_customer=pd.read_csv('D:\DT\DQ\CRM_coop\data\customer.txt',sep='\t',encoding = "ISO-8859-1")
df_order=df_order[['orderid','customerid','orderdate','totalprice']]
df=df_order.merge(df_customer[['customerid','householdid']],left_on='customerid',right_on='customerid')
df_1=df.groupby('householdid').orderdate.max().reset_index()
df_1.columns=[['householdid','max_date']]
df_1['recency']=(df_1['max_date'].max()-df_1['max_date']).apply(lambda x:x.dt.days)
#print(df_1)
#print(df['orderdate'].max(),df['orderdate'].min())

import datetime as dt
dt_prediction=dt.date(2016,10,1)
month_lookforward_range=[12]
#dt_model=dt.date(2016,7,1)
month_interval_range=[1]
month_offset_range=[36]

#we want to predict the clv in 2016-10
#dataset for prediction 2016 -06,07,08
#ds_pred=df[(df['orderdate'].dt.year==dt_prediction.year) & (df['orderdate'].dt.month==dt_prediction.month)]
#grid search
#month_lookforward=month_lookforward_range[0]
for month_interval in month_interval_range:
    for month_offset in month_offset_range:
        for month_lookforward in month_lookforward_range:

            dt_model=dt_prediction-relativedelta(months=month_interval+month_lookforward-1)
            print(f'dt_model-{dt_model}')
            ds_pred=df[(dt_prediction.year*12+dt_prediction.month-df['orderdate'].dt.year*12-df['orderdate'].dt.month>month_interval) &
                       (dt_prediction.year*12+dt_prediction.month-df['orderdate'].dt.year*12-df['orderdate'].dt.month<=month_offset+month_interval)]

            ds_pred = ds_pred.groupby('householdid').agg({
                'orderdate': lambda x: (ds_pred['orderdate'].max() - x.max()).days,
                'totalprice': 'sum', 'orderid': 'count'
            }).reset_index()
            ds_pred.columns = ['householdid', 'recency', 'monetary', 'frequency']

            #print(f"pred-{ds_pred['orderdate'].max()},{ds_pred['orderdate'].min()}")
            #dataset for build the model
            #x-input variables 2016-01,02,03,04,05,06
            #y-output variables 2016-08
            ds_input=df[(dt_model.year*12+dt_model.month-df['orderdate'].dt.year*12-df['orderdate'].dt.month>month_interval) &
                       (dt_model.year*12+dt_model.month-df['orderdate'].dt.year*12-df['orderdate'].dt.month<=month_offset+month_interval)]
            #print(ds_input['orderdate'].max(),ds_input['orderdate'].min())
            ds_input=ds_input.groupby('householdid').agg({
                                       'orderdate':lambda x:(ds_input['orderdate'].max()-x.max()).days,
                                       'totalprice':'sum','orderid':'count'
                                                          }).reset_index()
            ds_input.columns=['householdid','recency','monetary','frequency']
            #print(ds_input['orderdate'].max(),ds_input['orderdate'].min())
            print(dt_model.year,dt_model.month,month_lookforward)
            ds_output=df[(df['orderdate'].dt.year*12+df['orderdate'].dt.month-dt_model.year*12-dt_model.month>=0) &
                         (df['orderdate'].dt.year*12+df['orderdate'].dt.month-dt_model.year*12-dt_model.month<month_lookforward)]
            print(ds_output['orderdate'].max(), ds_output['orderdate'].min())
            ds_output.columns=[['orderid','customerid','orderdate','clv','householdid']]
            #print(ds_output)
            ds_output.columns=ds_output.columns.get_level_values(0)
            ds_output=ds_output.groupby('householdid').agg({
                                       'clv':'sum'
                                                          }).reset_index()
            ds_model=ds_input.merge(ds_output,on='householdid',how='left')
        #print(ds_model[~(ds_model['clv'].isna())]) imbalanced dataset:oversampling or undersampling
        print(month_interval,month_offset,ds_model.shape[0]-ds_model['clv'].isnull().sum())
print(ds_model)
ds_pred.to_csv('ds_pred_12mo.csv')
ds_model.to_csv('ds_model_36mo.csv')
#ds for training(x+y[2016-04,05,06,08],70%)
#ds for test(x+y[2016-04,05,06,08],30%)'''

