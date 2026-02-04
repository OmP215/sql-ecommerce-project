
-- Total revenue
select round(sum(oi.quantity * oi.unit_price * (1 - oi.discount/100)), 2) as total_revenue from orders o
	join order_items oi on o.order_id = oi.order_id where o.status in ('paid', 'shipped');

-- Revenue by day
select date(o.order_date) as order_day,
	round(sum(oi.quantity * oi.unit_price * (1-oi.discount/100)),2) as daily_revenue
	from orders o join order_items oi on o.order_id = oi.order_id where o.status in ('paid','shipped')
	group by date(o.order_date) order by order_day;

-- Revenue by category
select p.category, round(sum(oi.quantity * oi.unit_price * (1-oi.discount/100)),2) as category_revenue from orders o 
	join order_items oi on o.order_id = oi.order_id
	join products p on oi.product_id = p.product_id where o.status in ('paid','shipped') 
	group by p.category order by category_revenue desc;