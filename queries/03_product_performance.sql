-- Revenue, cost, and margin per poduct

select p.product_id, p.product_name, p.category,
	round(sum(oi.quantity * oi.unit_price * (1- oi.discount / 100)),2) as revenue,
	round(sum(oi.quantity * p.cost),2) as total_cost,
	round(sum(oi.quantity * oi.unit_price * (1- oi.discount/ 100)),2) - round(sum(oi.quantity * p.cost),2) as margin
	from products p
	join order_items oi on p.product_id = oi.product_id
	join orders o on oi.order_id = o.order_id
	where o.status in ('paid','shipped')
	group by p.product_id, p.product_name, p.category
	order by margin desc
	limit 20;
