# Retail Sales Forecasting & Analytics

## Project Overview

This project is an end-to-end retail sales forecasting and analytics project developed using Python, Machine Learning, SQL, and Streamlit.

The objective of this project is to analyze historical retail sales data, identify important business trends, and build a machine learning model to predict weekly sales.

An interactive dashboard was also created to make the analysis easy to understand for business users.

---

## Project Objectives

- Clean and preprocess raw retail sales data
- Merge multiple datasets into one analytical dataset
- Perform Exploratory Data Analysis (EDA)
- Identify top-performing stores and departments
- Analyze holiday and seasonal sales patterns
- Study the impact of external factors on sales
- Perform feature engineering
- Build a machine learning model for sales prediction
- Evaluate model performance
- Create an interactive Streamlit dashboard
- Perform business analysis using SQL

---

## Dataset

The project uses three main datasets:

### sales.csv
Contains historical retail sales information.

Important fields include:

- Store ID
- Department ID
- Date
- Weekly Sales
- Holiday Indicator

### features.csv
Contains external and economic features such as:

- Temperature
- Fuel Price
- CPI
- Unemployment
- Markdown information
- Holiday information
- Seasonal information

### stores.csv
Contains store-related information such as:

- Store ID
- Store Type
- Store Size

---

## Project Workflow

Raw Data  
↓  
Data Understanding  
↓  
Data Cleaning  
↓  
Data Integration  
↓  
Feature Engineering  
↓  
Exploratory Data Analysis  
↓  
Machine Learning  
↓  
Model Evaluation  
↓  
SQL Analysis  
↓  
Interactive Dashboard  
↓  
Business Insights

---

## Tools and Technologies Used

### Programming
- Python

### Data Analysis
- Pandas
- NumPy

### Data Visualization
- Matplotlib
- Seaborn
- Plotly

### Machine Learning
- Scikit-learn
- Random Forest Regressor

### Dashboard
- Streamlit
- Plotly

### Database Analysis
- SQL

### Development Tools
- VS Code
- Jupyter Notebook
- Git
- GitHub

---

## Data Cleaning and Preprocessing

The following preprocessing steps were performed:

- Checked dataset structure
- Standardized column names
- Converted date columns into datetime format
- Merged sales, features, and store datasets
- Checked and removed duplicate records
- Handled missing values
- Processed markdown columns
- Prepared a clean analytical dataset

---

## Feature Engineering

Additional features were created to improve analysis and forecasting:

- Year
- Month
- Week
- Quarter
- Day of Week
- Weekend Indicator
- Lag Sales Features
- Rolling Average Sales

These features help the model capture time-based and recent sales patterns.

---

## Exploratory Data Analysis

The EDA focuses on:

- Total retail sales
- Average weekly sales
- Store-wise performance
- Department-wise performance
- Monthly sales trends
- Weekly sales trends
- Holiday vs Non-Holiday sales
- External economic factors
- Correlation between numerical variables

---

## Machine Learning Model

A Random Forest Regressor was used to predict weekly retail sales.

A chronological train-test split was used instead of randomly shuffling the dataset.

This approach is more suitable for forecasting because future data should not be used to predict historical observations.

---

## Model Evaluation

The Random Forest model was evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

### Current Model Performance

- MAE: approximately 27,477
- RMSE: approximately 38,724
- R² Score: approximately 0.41

The model captures part of the variation in retail sales.

The model can be improved further through additional feature engineering, parameter tuning, and advanced forecasting techniques.

---

## Interactive Dashboard

An interactive dashboard was developed using Streamlit and Plotly.

The dashboard includes:

- Store selection filters
- Total Sales KPI
- Average Weekly Sales KPI
- Weekly Sales Trend
- Monthly Sales Trend
- Store Performance
- Top Departments
- Holiday vs Non-Holiday Analysis
- Machine Learning Performance Metrics
- Actual vs Predicted Sales
- Dataset Preview

The dashboard allows users to explore the retail data interactively.

---

## SQL Analysis

SQL queries were added to answer important retail business questions such as:

- Which stores generate the highest sales?
- Which departments perform best?
- How do holiday sales differ from non-holiday sales?
- How do sales change month by month?
- Which stores have the highest average weekly sales?
- What are the highest and lowest weekly sales values?

---

## Business Value

This project can help retail businesses:

- Improve sales forecasting
- Identify high-performing stores
- Identify high-performing departments
- Understand seasonal demand
- Prepare for holiday demand
- Improve inventory planning
- Improve resource allocation
- Support data-driven decision making

---

## Project Structure

```text
retail-sales-forecasting/
│
├── archive/
│   ├── features.csv
│   ├── sales.csv
│   └── stores.csv
│
├── data/
│   └── processed/
│       └── clean_retail_sales.csv
│
├── notebook/
│   └── retail_sales_eda.ipynb
│
├── models/
│   ├── model_features.pkl
│   └── random_forest_sales_model.pkl
│
├── output/
│   ├── sales_predictions.csv
│   └── sales_predictions_enriched.csv
│
├── dashboard/
│   └── app.py
│
├── sql/
│   └── retail_analysis.sql
│
├── image.png
├── README.md
├── requirements.txt
└── .gitignore