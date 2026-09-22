# Kimball Business Modeling Notes

## Business Process

Customers place orders and purchase products on Olist platform

## Grain

1 row = one order item within one order (order_id + order_item_id is unique identifier)

Reason: order_id is duplicated 13984 times in the order_items table, found when exploring data, which means there could be multiple items within one order and order_id should not be the grain.

## Dimensions

- dim_customers：customer info (address needs to be tracked → SCD Type 2)
- dim_products：product info
- dim_sellers：seller info
- dim_date：date dimension

## Facts

- price - addable
- freight_value - addable

## Degenerate Dimension

order_id (remain in the fact table, no separate dimension table)

## 关联关系验证

- order_items 与 orders 通过 order_id 关联，孤儿记录数 = 0（可以安全join，不会丢数据）
- orders表本身 order_id 无重复（订单级粒度，符合预期）

## Bus Matrix

| Business Process  | Dim Customer | Dim Products | Dim Seller | Dim Date |
| ----------------- | ------------ | ------------ | ---------- | -------- |
| Order item detail | ✓            | ✓            | ✓          | ✓        |

<!-- customer_id：每次下单都会生成一个新的customer_id，即使是同一个真人反复下单
customer_unique_id：代表真正的同一个自然人，跨多个订单不变 -->
