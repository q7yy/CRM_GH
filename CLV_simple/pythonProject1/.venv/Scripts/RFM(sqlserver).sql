
select concat(rencency,money,freq) as rmf,r,m,f,rencency,money,freq
from (
select householdid,
ntile(3) over (order by r asc ) as rencency,
ntile(3) over (order by m desc) as money,
ntile(3) over (order by f desc) as freq,r,m,f
from
(
select householdid,DATEDIFF(dd,max(orderdate),'2016-01-01') as r,
sum(totalprice)/count(orderid) as m,
count(orderid)/DATEDIFF(dd,max(orderdate),'2016-01-01') as f
from
(select orders.*,householdid from orders,customers
where orders.customerid=customers.customerid
and datediff(dd,orderdate,'2016-01-01') > 0 )customer_orders

group by householdid

)rfm_score


)rfm
group by concat(rencency,money,freq)
order by concat(rencency,money,freq)




