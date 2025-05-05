select * from users_user;

select * from carts_cart;
select * from carts_item;
select * from carts_cart_items;


select * from orders_orderlist;
select * from orders_orderlist_orders;
select * from orders_order;
select * from orders_order_item;
select * from orders_order_items;

select * from products_product;

-- delete from orders_orderlist;


SELECT
    c.id AS cart_id,
    u.id AS user_id,
	c.cart_total,
	c.updated_at,
    i.id AS item_id,
    i.quantity,
    i.item_total,
    p.id AS product_id,
    p.name AS product_name,
    p.price AS product_price,
	p.stock AS product_stock
FROM carts_cart c
JOIN users_user u ON c.user_id = u.id
JOIN carts_cart_items ci ON c.id = ci.cart_id
JOIN carts_item i ON ci.item_id = i.id
JOIN products_product p ON i.product_id = p.id;