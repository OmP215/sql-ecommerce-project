-- view recent active customers
create or replace view active_custoemrs_last_90_days as
select distinct
	c.customer_id,
	c.first_name,
    c.last_name,
    c.email,
    c.region,
    c.acquistion_channel
from customers c
join orders o on c.customer_id = o.customer_id
where o.order_date >= NOW() - INTERVAL '90 Days'
and o.status in ('paid','shipped');

-- view orders with revenuw and margin
create or replace view orders_wth_margins as
select
	o.order_id,
    o.customer_id,
    o.order_date,
    o.status,
    sum(oi.quantity * oi.unit_price * (1 - oi.discount / 100.0)) as revenue,
    sum(oi.quantity * p.cost) as cost,
    sum(oi.quantity * oi.unit_price * (1 - oi.discount / 100.0)) -
    sum(oi.quantity * p.cost) as margin
from orders o
join order_items oi on o.order_id = oi.order_id
join products p on oi.product_id = p.product_id
group by o.order_id, o.customer_id, o.order_date, o.status;


