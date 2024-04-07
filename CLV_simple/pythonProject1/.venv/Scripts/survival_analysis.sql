UPDATE sqlbook.subs SET stop_date = NULL WHERE stop_date = 0000-00-00;
UPDATE sqlbook.subs SET start_date = NULL WHERE start_date = 0000-00-00;

SELECT max(start_date),min(start_date),max(stop_date),min(stop_date) FROM sqlbook.subs;

select * from sqlbook.subs where customer_id=54449481;
select min(start_date),min(stop_date),max(start_date),max(stop_date) FROM sqlbook.subs;

select distinct stop_type from subs;


select customer_id,tenure,
datediff(case when stop_date is null then cut_off else stop_date end,start_date),
start_date,stop_date,stop_type
from
subs,
(select min(start_date),min(stop_date),
max(start_date),max(stop_date) as cut_off FROM sqlbook.subs) subs_date;

#hazard probability when the cutoff is 100 days
select 
sum(case when tenure=100 and stop_date is not null then 1 else 0 end) as num_faillure,
count(*) as num_pop,
sum(case when tenure=100 and stop_date is not null then 1 else 0 end) /count(*) as h_100
from subs
where tenure>=100;

select tenure,
count(*) as pop_tenure,
sum(case when stop_date is not null then 1 else 0 end) as faillure_tenure
from subs
where tenure>=0 and datediff('2004-01-01',start_date)<=0
group by tenure
;
#retention
select datediff('2006-12-28',start_date) as cal_dates,count(*),
avg(case when stop_date is null then 1 else 0 end) as retention_rate
from subs
where tenure>=0 and datediff('2004-01-01',start_date)>=0
group by datediff('2006-12-28',start_date) ;

