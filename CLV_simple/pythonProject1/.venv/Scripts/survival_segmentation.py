import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv('../Lib/site-packages/subs.txt', sep='\t', encoding ="ISO-8859-1", parse_dates=['start_date', 'stop_date'])
df=df.loc[(df.tenure>=0)&(df.start_date>='2004-01-01')]
df['churned']=df['stop_type'].apply(lambda x : 0 if pd.isnull(x) else 1)

#df=df[['rate_plan','monthly_fee','market','channel','tenure','churned']] (by dummy var)
'''which rate plan has a better performance on churn management?(log rank/hazard ratio)
    which factor is more significant for churn management?(cox proportional hazard model)
by Sql: select distinct rate_plan from subs;

df_b=df.loc[df.rate_plan=='Bottom']
df_t=df.loc[df.rate_plan=='Top']
df_m=df.loc[df.rate_plan=='Middle']
kmf_t=KaplanMeierFitter()
kmf_m=KaplanMeierFitter()
kmf_b=KaplanMeierFitter()
kmf_t.fit(durations=df_t['tenure'],event_observed=df_t['churned'],label="Top")
kmf_m.fit(durations=df_m['tenure'],event_observed=df_m['churned'],label="Middle")
kmf_b.fit(durations=df_b['tenure'],event_observed=df_b['churned'],label="Bottom")

kmf_t.plot_survival_function()
kmf_b.plot_survival_function()
kmf_m.plot_survival_function()

plt.show()

from lifelines.statistics import logrank_test
results=logrank_test(df_t['tenure'],df_b['tenure'],df_t['churned'],df_b['churned'])
results.print_summary()
print(results.p_value)
print(results.test_statistic)'''

df=df[['monthly_fee','tenure','churned']]
print(df)
'''from lifelines.datasets import load_rossi
from lifelines import CoxPHFitter
cph=CoxPHFitter()
cph.fit(df,'tenure','churned')
cph.print_summary()
cph.plot()
cph.show()'''


