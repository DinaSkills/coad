import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db.setup_database import db_create
from db.populate_db import populateDB

# Connect to the database
db_name = 'db/customer_orders.db'
conn = db_create(db_name)
conn.create_table_from_txt('db/table_schema.txt')
add_data = populateDB(conn, use_csv=True, csv_path='db/full_sample_orders.csv')

st.title("Customer Orders Analytics Dashboard")

# Load data
customers = pd.read_sql_query("SELECT * FROM customers", conn.conn)
orders = pd.read_sql_query("SELECT * FROM orders", conn.conn)
order_details = pd.read_sql_query("SELECT * FROM order_details", conn.conn)
products = pd.read_sql_query("SELECT * FROM products", conn.conn)

# Merge data for analysis
merged_df = pd.merge(orders, order_details, on="order_id")
merged_df = pd.merge(merged_df, customers, on="customer_id")
merged_df = pd.merge(merged_df, products, on="product_id")

# Show total orders per customer
st.subheader("Total Orders per Customer")
orders_per_customer = merged_df.groupby('name')['order_id'].count().reset_index().rename(columns={
    'name': 'Customer Name', 'order_id': 'Total orders'})

st.write(orders_per_customer)

# Plot top 5 products sold
st.subheader("Top 5 Products Sold")
top_products = merged_df['product_name'].value_counts().head(5)
fig, ax = plt.subplots()
top_products.plot(kind='bar', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot order trends over time
st.subheader("Order Trends Over Time")
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])
orders_over_time = merged_df.groupby(merged_df['order_date'].dt.date).size()
fig, ax = plt.subplots()
orders_over_time.plot(kind='line', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

conn.close()
