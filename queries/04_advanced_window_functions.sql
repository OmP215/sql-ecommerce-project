-- Revenue per customer per month with a rank in that month

with monthly_customer_revenue as (
	select date_trunc('month', o.order_date) as order_month,
	c.customer_id,
	concat(c.first_name, ' ', c.last_name) as customer_name,
	round(sum(oi.quantity * oi.unit_price * (1 - oi.discount / 100)),2) as revenue
	from orders o
	join order_items oi on o.order_id = oi.order_id
	join customers c on o.customer_id = c.customer_id
	where o.status in ('paid','shipped')
	group by order_month, c.customer_id, customer_name
)

select order_month::date, customer_id, customer_name, revenue,
	rank() over (partition by order_month order by revenue desc) as rev_rank_in_month
	from monthly_customer_revenue
	order by order_month, rev_rank_in_month
	limit 100;


-- Rolling 7-day revenue window
with daily_revenue as (
	select date(order_date) as order_day, 
	sum(oi.quantity * oi.unit_price * (1 - oi.discount / 100.0)) as revenue
	from orders o join order_items oi on o.order_id = oi.order_id
	where o.status in ('paid', 'shipped') group by date(order_date)
)
select order_day, revenue, sum(revenue) over (
	order by order_day
	rows between 6 preceding and current row
) as rolling_7d_revenue
from daily_revenue
order by order_day;