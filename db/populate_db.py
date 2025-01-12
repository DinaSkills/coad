import sqlite3
import random
from datetime import datetime, timedelta

import pandas as pd


class populateDB:

    def __init__(self, conn, use_csv=False, csv_path=None):
        self.conn = conn
        self.c = self.conn.conn.cursor()

        if use_csv and csv_path:
            self.load_data_from_csv(csv_path)
        else:
            self.add_sample_customers()
            self.add_sample_product()
            self.add_sample_orders()

    def add_sample_customers(self):

        customers = [
            ('Alice Johnson', 'alice@example.com'),
            ('Bob Smith', 'bob@example.com'),
            ('Charlie Brown', 'charlie@example.com')
        ]
        self.c.executemany('INSERT INTO customers (name, email) VALUES (?, ?)', customers)

    def add_sample_product(self):
        # Add sample products
        products = [
            ('Laptop', 'Electronics'),
            ('Phone', 'Electronics'),
            ('Headphones', 'Accessories'),
            ('Book', 'Books'),
            ('Shoes', 'Fashion')
        ]
        self.c.executemany('INSERT INTO products (product_name, category) VALUES (?, ?)', products)

    def add_sample_orders(self):

        for i in range(1, 6):
            customer_id = random.choice([1, 2, 3])
            order_date = datetime.now() - timedelta(days=random.randint(1, 30))
            self.c.execute('INSERT INTO orders (customer_id, order_date) VALUES (?, ?)',
                      (customer_id, order_date.strftime('%Y-%m-%d')))

            order_id = self.c.lastrowid
            for _ in range(random.randint(1, 3)):
                product_id = random.choice([1, 2, 3, 4, 5])
                quantity = random.randint(1, 5)
                self.c.execute('INSERT INTO order_details (order_id, product_id, quantity) VALUES (?, ?, ?)',
                          (order_id, product_id, quantity))

    def clean_data(self, df):
        """Perform basic data cleaning."""
        # Drop duplicates
        df = df.drop_duplicates()


        df.fillna({
            'name': 'Unknown',
            'email': 'unknown@example.com',
            'product_name': 'Miscellaneous',
            'category': 'Unknown',
            'order_date': datetime.now().strftime('%Y-%m-%d'),
            'quantity': 1,
        }, inplace=True)


        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date']).dt.strftime('%Y-%m-%d')

        return df

    def load_data_from_csv(self, file_path):
        """Load and clean data from a CSV file."""
        df = pd.read_csv(file_path)
        df = self.clean_data(df)

        # Split data into appropriate tables
        customers = df[['customer_id', 'name', 'email']].drop_duplicates(subset='customer_id')
        products = df[['product_id', 'product_name', 'category']].drop_duplicates(subset='product_id')
        orders = df[['order_id', 'customer_id', 'order_date']].drop_duplicates(subset='order_id')
        order_details = df[['order_detail_id', 'order_id', 'product_id', 'quantity']].drop_duplicates(
            subset='order_detail_id')

        self.insert_with_conflict_handling(customers, 'customers', self.conn.conn, 'customer_id')
        self.insert_with_conflict_handling(products, 'products', self.conn.conn, 'product_id')
        self.insert_with_conflict_handling(orders, 'orders', self.conn.conn, 'order_id')
        self.insert_with_conflict_handling(order_details, 'order_details', self.conn.conn, 'order_detail_id')

        print("Data loaded successfully!")

    def insert_with_conflict_handling(self, df, table_name, conn, conflict_column):
        for index, row in df.iterrows():
            query = f"""
            INSERT INTO {table_name} ({', '.join(row.index)}) 
            VALUES ({', '.join(['?'] * len(row))})
            ON CONFLICT({conflict_column}) DO NOTHING
            """
            conn.execute(query, tuple(row))
        conn.commit()

