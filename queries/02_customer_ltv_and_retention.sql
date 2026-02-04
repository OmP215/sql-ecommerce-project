 -- Lifetime Value per customer
 with customer_revenue as (
	select c.customer_id, concat(c.first_name, ' ', c.last_name) as customer_name,
	sum(oi.quantity * oi.unit_price *(1 - oi.discount / 100)) as ltv
	from customers c
	join orders o on c.customer_id = o.customer_id
	join order_items oi on o.order_id = oi.order_id
	where o.status in ('paid','shipped')
	group by c.customer_id, customer_name
 )

 select * from customer_revenue order by ltv desc limit 20;