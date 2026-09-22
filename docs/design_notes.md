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

## SCD Type 2 实现与踩坑记录

- 最初尝试直接用customer_unique_id作为snapshot的unique_key，
  发现该字段在raw_customers中并非唯一（同一人多次下单产生多行地址相同的记录），
  导致snapshot误判大量记录发生变化（INSERT 275而非预期的1条）
- 解决方式：新增stg_customers_unique模型，用窗口函数row_number()按
  customer_unique_id去重，只保留每个真实客户的一条代表记录，再基于此做snapshot
- 验证SCD2效果：手动修改raw表中一个客户的城市字段，重跑staging+去重模型+snapshot，
  确认同一customer_unique_id在快照表中正确生成了两条历史记录
  （旧值dbt_valid_to有终止时间，新值dbt_valid_to为NULL代表当前有效）
