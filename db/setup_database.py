import sqlite3
from symtable import Class


class db_create:
    # Create a database and tables
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def create_tables(self, table_name, **kwargs):
        columns = ', '.join([f'{key} {value}' for key, value in kwargs.items()])
        self.c.execute(f'CREATE TABLE {table_name} ({columns})')

    def create_table_from_txt(self, file_path):
        """
            Read table schemas from a text file and create tables in the database.
            The text file should define each table schema with the following format:

            table_name: customers
            customer_id INTEGER PRIMARY KEY
            name TEXT NOT NULL
            email TEXT UNIQUE NOT NULL

            table_name: orders
            order_id INTEGER PRIMARY KEY
            customer_id INTEGER NOT NULL
            order_date TEXT NOT NULL
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            """
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                table_definitions = {}
                current_table = None

                # Parse the text file
                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line:
                        if stripped_line.startswith('table_name'):
                            # Start a new table definition
                            current_table = stripped_line.split(':')[1].strip()
                            table_definitions[current_table] = []
                        else:
                            # Add column or constraint definitions to the current table
                            if current_table:
                                table_definitions[current_table].append(stripped_line)

                # Execute CREATE TABLE statements
                for table_name, columns in table_definitions.items():
                    columns_sql = ', '.join(columns)
                    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql})"
                    self.c.execute(create_table_sql)

            self.conn.commit()
            print("Tables created successfully from schema file.")

        except Exception as e:
            print(f"An error occurred: {e}")

    def insert_table_from_txt(self, file_path):
        # Read the table data from a text file and insert data into the tables
        with open(file_path, 'r') as file:
            lines = file.readlines()
            table_data = {}
            current_table = None

            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith('table_name:'):
                    current_table = stripped_line.split(':')[1].strip()
                    table_data[current_table] = []
                elif stripped_line and current_table:
                    table_data[current_table].append(tuple(stripped_line.split(',')))

            for table_name, rows in table_data.items():
                placeholders = ', '.join(['?' for _ in rows[0]])
                insert_sql = f"INSERT OR IGNORE INTO {table_name} VALUES ({placeholders})"
                self.c.executemany(insert_sql, rows)
            self.conn.commit()

    @staticmethod
    def db_exists(db_name):
        try:
            conn = sqlite3.connect(db_name)
            conn.close()
            return True
        except sqlite3.Error:
            return

    def close(self):
        self.conn.close()



