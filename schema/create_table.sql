--drop tables for easy reruns
drop table if exists order_items;
drop table if exists orders;
drop table if exists web_sessions;
drop table if exists products;
drop table if exists customers;

--customers table
create table customers (
	customer_id 	serial primary key,
	first_name 		varchar(50),
	last_name 		varchar(50),
	email 			varchar(100) not null,
	signup_date		date not null,
	region			varchar(50),
	acquistion_channel	varchar(50),
	is_active		boolean default TRUE
);

--products table
create table products(
	product_id		serial primary key,
	product_name	varchar(100) not null,
	category		varchar(50) not null,
	subcatefory		varchar(50),
	price			numeric(10,2) not null check (price >=0),
	cost			numeric(10,2) not null check (cost >=0),
	is_discontinued	boolean default false
);

--orders table
create table orders(
	order_id 		serial primary key,
	customer_id		integer not null references customers(customer_id),
	order_date		timestamp not null,
	status			varchar(20) not null check (status in ('pending', 'paid', 'shipped', 'cancelled', 'refunded')),
	payment_method	varchar(30),
	shipping_country varchar(50),
	shipping_city	varchar(50)
);

--order_items table
create table order_items(
	order_item_id	serial primary key,
	order_id		integer not null references orders(order_id) on delete cascade,
	product_id		integer not null references products(product_id),
	quantity		integer not null check (quantity > 0),
	unit_price		numeric(10,2) not null check (unit_price >= 0),
	discount		numeric(5,2) not null default 0 check (discount >=0) -- percent 0-100
);

--web_sessions table
create table web_sessions(
	session_id		serial primary key,
	customer_id		integer references customers(customer_id),
	session_start	timestamp not null,
	device_type		varchar(30),	--'desktop', 'mobile', etc
	traffic_source	varchar(50),	--'email', 'paid social', etc
	landed_on_page	varchar(100)	--'product', 'home', 'cart'
);