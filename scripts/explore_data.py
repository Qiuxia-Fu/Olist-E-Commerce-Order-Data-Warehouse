import pandas as pd

files = [
    "olist_orders_dataset",
    "olist_order_items_dataset",
    "olist_customers_dataset",
    "olist_products_dataset",
    "olist_sellers_dataset",
    "olist_order_payments_dataset",
]

for f in files:
    df = pd.read_csv(f"raw_data/{f}.csv")
    print(f"=== {f} ===")
    # print(df.shape)          # (行数, 列数)，比len(df)信息更全
    # print(df.info())         # 一次性看到列名、类型、有没有缺失值，比dtypes+head分开看更高效
    # print(df.describe())     # 数值列的统计概况（均值、最大最小值等），一眼看出异常值
    # print(df.head(2))
    print(df.isnull().sum())        # 每列有多少个空值
    print(df.duplicated().sum())    # 有多少完全重复的行
    # 某个理论上应该唯一的字段，实际有没有重复——这个非常重要，直接关系到你的grain判断对不对

# 下面是只针对特定表的检查，单独拿出来，不放进上面的通用循环
df_orders = pd.read_csv("raw_data/olist_orders_dataset.csv")
print("=== orders表专项检查 ===")
# 预期应该是0，因为orders表粒度是订单级
print(f"order_id重复数: {df_orders['order_id'].duplicated().sum()}")
print(df_orders['order_status'].value_counts())

df_items = pd.read_csv("raw_data/olist_order_items_dataset.csv")
print("=== order_items表专项检查 ===")
# 预期会有大量重复，因为一个订单多个商品
print(f"order_id重复数: {df_items['order_id'].duplicated().sum()}")

# 关联关系验证：order_items里的order_id，是否都能在orders表里找到
orphan = df_items[~df_items['order_id'].isin(df_orders['order_id'])]
print(f"order_items里找不到对应订单的孤儿记录数: {len(orphan)}")   # 预期应该是0

# print(df['order_id'].duplicated().sum())
# print(df['order_status'].value_counts())   # 比如看订单状态有哪几种取值，各有多少个
# print(df['order_status'].unique())         # 只看有哪些不重复的值，不看数量
