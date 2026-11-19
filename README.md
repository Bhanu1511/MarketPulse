📊 MarketPulse – Business & Customer Intelligence Platform

MarketPulse is an interactive Business Intelligence and Customer Analytics platform built using Python, SQL, PostgreSQL and Streamlit.

The project analyses Brazilian e-commerce data to uncover business trends, understand customer behaviour, evaluate product performance and identify operational improvements.

🚀 Project Overview

MarketPulse transforms raw e-commerce data into meaningful business insights through data cleaning, SQL analysis, Python visualisations and an interactive dashboard.

Key Features

* Business Overview: Revenue, delivered orders, customer and operational KPIs.
* Revenue Analytics: Monthly revenue trends and top-performing product categories.
* Customer Analytics: Customer segmentation and RFM analysis.
* Operations Analytics: Delivery performance and customer satisfaction.
* Interactive Dashboard: Filters, visualisations and downloadable analysis data.

🛠️ Tech Stack

Technology	Purpose
Python	Data analysis and processing
Pandas & NumPy	Data cleaning and manipulation
PostgreSQL	Relational database
SQL	Business queries and analysis
Matplotlib & Seaborn	Data visualisation
Plotly	Interactive charts
Streamlit	Dashboard development

📈 Key Business Insights

* Total delivered orders analysed: 96,470.
* Unique customers analysed: 93,358.
* Average review score: 4.09/5.
* On-time delivery rate: 91.88%.
* Late delivery rate: 8.12%.
* Repeat customer rate: Approximately 3%.

Additional Findings

* Health & Beauty was the highest-revenue product category.
* November 2017 recorded the highest monthly revenue.
* Customers receiving late deliveries had a lower average review score (2.57) than customers receiving on-time deliveries (4.29).

📂 Project Structure

MarketPulse/
│
├── dashboard/
│   ├── app.py
│   └── .streamlit/
│
├── data/
│   ├── cleaned/
│   └── analysis_outputs/
│
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_database_integration.ipynb
│   ├── 04_python_visualization.ipynb
│   └── 05_export_analysis.ipynb
│
├── reports/
│
├── sql/
│
├── requirements.txt
└── README.md

⚙️ How to Run the Project

1. Clone the repository

git clone https://github.com/Bhanu1511/MarketPulse.git
cd MarketPulse

2. Create a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run the dashboard

streamlit run dashboard/app.py

The dashboard will open in your browser at:

http://localhost:8501

📊 Dataset

The project uses the Brazilian E-Commerce Public Dataset by Olist.

The original dataset contains information about customers, orders, payments, products, sellers, reviews and delivery performance.

🎯 Project Objective

To demonstrate practical Data Analytics skills by converting raw business data into actionable insights using SQL, Python, PostgreSQL and interactive visualisation.

⸻

Developed as a Data Analytics Portfolio Project.