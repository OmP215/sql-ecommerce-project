-- Useful indexes
create index idx_orders_customer_date on orders (customer_id, order_date);

create index idx_orders_status_date on orders (status, order_date);

create index idx_order_items_order on order_items (order_id);

create index idx_order_items_products on order_items (product_id);

create index idx_products_category on products (category);

explain analyze 
select date(o.order_date) as order_day,
	sum(oi.quantity *oi.unit_price * (1 - oi.discount / 100)) as daily_revenue
	from orders o join order_items oi on o.order_id = oi.order_id
	where o.status in ('paid','shipped') group by date(o.order_date) order by order_day;