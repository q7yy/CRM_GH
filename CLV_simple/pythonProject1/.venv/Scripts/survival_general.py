import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('../Lib/site-packages/subs.txt', sep='\t', encoding ="ISO-8859-1", parse_dates=['start_date', 'stop_date'])
'''print(df.describe())
print(df.shape)
print(df.dtypes)
print(df.columns)
df['rate_plan'].hist()
plt.show()'''
df=df.loc[(df.tenure>=0) & (df.start_date >='2004-01-01')]
df['churned']=df['stop_type'].apply(lambda x: 0 if pd.isnull(x) else 1)
print(df[['churned','censored']])
#cumulative hazard function
'''from lifelines import NelsonAalenFitter
naf=NelsonAalenFitter()
naf.fit(durations=df['tenure'],event_observed=df['churned'])
naf.cumulative_hazard_
naf.plot_cumulative_hazard()
plt.show()'''
#survival function
from lifelines import KaplanMeierFitter
kmf=KaplanMeierFitter()
kmf.fit(durations=df['tenure'],event_observed=df['churned'])
print(kmf.survival_function_)
kmf.plot_survival_function()
plt.show()
'''which rate plan has a better performance on churn management?(log rank/hazard ratio)
    which factor is more significant for churn management?(cox proportional hazard model)'''