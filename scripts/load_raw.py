from sqlalchemy import create_engine, text
import pandas as pd

engine = create_engine(
    "postgresql+psycopg2://dbt_user:dbt_pass@localhost:5433/olist")

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

files = {
    "raw_orders": "olist_orders_dataset.csv",
    "raw_order_items": "olist_order_items_dataset.csv",
    "raw_customers": "olist_customers_dataset.csv",
    "raw_products": "olist_products_dataset.csv",
    "raw_sellers": "olist_sellers_dataset.csv",
    "raw_payments": "olist_order_payments_dataset.csv",
}

for table, fname in files.items():
    df = pd.read_csv(f"raw_data/{fname}")
    df.to_sql(table, engine, schema="raw", if_exists="replace", index=False)
    print(f"loaded {table}: {len(df)} rows")
