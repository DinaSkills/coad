# Customer Orders Analytics Dashboard

Welcome to the Customer Orders Analytic dashboard project!

## Latest Release: 1.0.0

![Release](https://img.shields.io/badge/release-v2.6.5-brightgreen)

This project demonstrates a simple ETL pipeline integrated with an interactive dashboard to analyze customer orders from an e-commerce dataset. The application showcases data processing, SQL querying, and visualization using Python and Streamlit.

## Features
# ETL Pipeline
- Extract: Pulls raw data from CSV file.
- Transforms
   - Cleans and validates the data. 
   - Handles missing values and duplicates.
- Load: Stores the transformed data into a relational database for structured analysis.

## Interactive Dashboard

- Total Orders Per Customer: Displays the number of orders placed by each customer.
- Top 5 Products Sold: Visualizes the most popular products using a bar chart.
- Order Trends Over Time: Plots order trends to show activity across dates.

## Database Design
- Utilizes normalized tables for customers, products, orders, and order details.

## Technologies
- Python: For data extraction, transformation, and application development.
- SQLite:  As the relational database.
- Streamlit: For building the interactive dashboard.
- Pandas: For data manipulation and analysis.
- Matplotlib: For data visualization.

## Setup and Installation
 
### Prerequisites
- Python 3.7 or higher.
- Git installed on your system.
- A code editor like Visual Studio Code or PyCharm.
- Basic knowledge of Python and SQL.

### Steps to Set Up the Project
1. Clone the repository to your local machine.
```bash
  git clone https://github.com/your-username/customer-orders-dashboard.git
  cd customer-orders-dashboard
```
### 2. Set Up Virtual Environment:
```bash
  python3 -m venv venv
  source venv/bin/activate # For Linux/Mac
  venv\Scripts\activate # For Windows
```
### 3. Install Required Packages:
```bash
  pip install -r requirements.txt
```
### 4. Run the ETL Pipeline:

```bash
  streamlit run app.py
```
```bash
customer-orders-dashboard/
├── app.py # Streamlit dashboard application
    ├── db 
	  ├── setup_database.py      # Script to set up database schema
	  ├── populate_database.py   # Script to populate database with sample data
	  ├── customer_orders.db     # SQLite database (auto-generated)
├── requirements.txt       # List of required Python packages
└──README.md              # Project documentation

```
## How the ETL Pipeline Works
### 1. Extract

Data is extracted from CSV files, APIs, or generated as synthetic sample data.

### 2. Transform

- Data is cleaned, validated, and prepared for analysis:

- Duplicate records are removed.

- Missing values are handled.

- Relationships between datasets are established.

### 3. Load

Transformed data is loaded into an SQLite database for structured storage and querying.

## Dashboard Insights

### 1. Total Orders Per Customer

Displays the number of orders placed by each customer.

### 2. Top 5 Products Sold

Visualizes the most popular products using a bar chart.

### 3. Order Trends Over Time

Shows the number of orders placed over a period using a line chart.

## Future Enhancements

- Implement CSV upload for data extraction.

- Integrate a cloud-based database like PostgreSQL for scalability.

- Add real-time data streaming for live updates.

- Provide export options (e.g., CSV or Excel) for analysis results.


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request with your changes.


