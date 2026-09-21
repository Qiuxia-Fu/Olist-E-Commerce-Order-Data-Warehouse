# Kimball建模设计笔记

## 业务过程（Business Process）

客户在Olist平台下单购买商品

## 粒度（Grain）

一行 = 一个订单里的一个商品行项（order_id + order_item_id 唯一确定一行）

**验证依据**：探索数据时发现，order_items表里order_id有13984次重复
（说明确实存在一单多件商品的情况，不能用订单级粒度，否则会丢失"每件商品"这个层面的信息）

## 维度（Dimensions）

- dim_customers：客户信息（含地址，需要追踪历史变更 → SCD Type 2）
- dim_products：商品信息
- dim_sellers：卖家信息
- dim_date：日期维度

## 事实（Facts）

- price（商品单价）—— 可加事实
- freight_value（运费）—— 可加事实

## 退化维度（Degenerate Dimension）

order_id 保留在事实表里，不单独建维度表

## 关联关系验证

- order_items 与 orders 通过 order_id 关联，孤儿记录数 = 0（可以安全join，不会丢数据）
- orders表本身 order_id 无重复（订单级粒度，符合预期）

## 总线矩阵

| 业务过程     | 客户维度 | 商品维度 | 卖家维度 | 日期维度 |
| ------------ | -------- | -------- | -------- | -------- |
| 订单商品明细 | ✓        | ✓        | ✓        | ✓        |
