# SQL Customer Analytics Project

## Overview

This project demonstrates advanced SQL analytics using a relational database to answer real-world business questions about **revenue, profitability, and customer behavior**. The focus is on writing clean, performant SQL queries and using PostgreSQL features such as **CTEs, window functions, aggregations, and stored procedures**.

The project simulates an e-commerce environment with customers placing orders for products, allowing for analysis at the **product**, **order**, and **customer** levels.

---

## Key Business Questions Answered

* Which products generate the most revenue and profit?
* What are the total costs and margins per product?
* Who are the highest-value customers?
* What is the **lifetime value (LTV)** of each customer?
* How does discounting affect revenue and margin?

---

## Dataset Schema

The database consists of the following core tables:

### `customers`

* `customer_id` (PK)
* `first_name`
* `last_name`
* `email`
* `created_at`

### `orders`

* `order_id` (PK)
* `customer_id` (FK)
* `order_date`
* `status` (`paid`, `shipped`, `cancelled`, etc.)

### `order_items`

* `order_item_id` (PK)
* `order_id` (FK)
* `product_id` (FK)
* `quantity`
* `unit_price`
* `discount` (percentage)

### `products`

* `product_id` (PK)
* `product_name`
* `category`
* `cost` (unit cost)

---

## Example Analytics Queries

### Revenue, Cost, and Margin per Product

```sql
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount / 100.0)), 2) AS revenue,
    ROUND(SUM(oi.quantity * p.cost), 2) AS total_cost,
    ROUND(
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount / 100.0))
        - SUM(oi.quantity * p.cost),
        2
    ) AS margin
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status IN ('paid', 'shipped')
GROUP BY p.product_id, p.product_name, p.category
ORDER BY margin DESC
LIMIT 20;
```

---

## Customer Lifetime Value (LTV)

Customer Lifetime Value represents the **total revenue a customer has generated over their lifetime**, based on completed orders.

### Stored Function: Customer LTV

```sql
CREATE OR REPLACE FUNCTION get_customer_ltv(p_customer_id INTEGER)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $func$
BEGIN
    RETURN (
        SELECT COALESCE(
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount / 100.0)),
            0
        )
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.customer_id = p_customer_id
          AND o.status IN ('paid', 'shipped')
    );
END;
$func$;
```

### Example Usage

```sql
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    get_customer_ltv(c.customer_id) AS lifetime_value
FROM customers c
ORDER BY lifetime_value DESC;
```

---

## Technologies Used

* **PostgreSQL** (local development environment)
* **SQL / PLpgSQL**
* pgAdmin for query execution and development

---

## Skills Demonstrated

* Relational data modeling
* Complex SQL joins and aggregations
* Window functions and analytical queries
* Stored procedures and functions
* Business metric design (revenue, margin, LTV)
* Query correctness and numerical precision

---

## Potential Improvements

* Add time-based LTV (monthly / cohort-based analysis)
* Introduce indexes and compare query performance
* Connect to a BI tool (Tableau / Power BI)
* Containerize with Docker for portability

---

## Author

Om Patel

---

This project was designed to showcase SQL proficiency and analytical thinking for data-focused and software engineering roles.
