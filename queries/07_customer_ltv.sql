create or replace function get_customer_ltv(p_customer_id integer)
returns NUMERIC
language plpgsql
as $func$
begin
    return (
        select coalesce(
            sum(oi.quantity * oi.unit_price * (1 - oi.discount / 100.0)), 0)
        from orders o
        join order_items oi on o.order_id = oi.order_id
        where o.customer_id = p_customer_id
          and o.status in ('paid', 'shipped')
    );
end;
$func$;

select get_customer_ltv(1);