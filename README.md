NEPSE Stock Analyzer (SARBTM)
This project provides a Streamlit-based web application to analyze the stock data of Sarbottam Cement Limited (SARBTM) from the Nepal Stock Exchange (NEPSE). It displays company profiles, recent news, price history, and offers a basic prediction of future stock prices using a linear regression model.

Table of Contents
Features

Project Structure

Setup Instructions

Prerequisites

Database Setup (XAMPP MySQL)

Python Environment Setup

Running the Application

Data Sources

Machine Learning Model

Customization

Troubleshooting

Contributing

License

Features
Company Profile: Displays key information about Sarbottam Cement Limited (SARBTM), including its name, symbol, sector, shares outstanding, market price, EPS, PE ratio, and contact details.

Latest News: Shows recent news articles related to SARBTM, fetched from a CSV file.

Price History: Presents historical daily price data (Open, High, Low, Close, Volume) for SARBTM.

Price Prediction: Utilizes a simple linear regression model to predict the closing prices for the next 5 trading days. Includes model performance metrics (MSE, R2).

Data Refresh: A "Refresh Data" button in the sidebar allows users to clear cached data and reload all information.

Styling: Custom CSS for an improved user interface.

Project Structure
The project consists of several Python scripts and a dedicated folder for scraped data:

├── a.py
├── project.py (This file is named `model.py` in your provided code, but functions as `predict_future_prices`)
├── model.py (This file is named `mysql_db.py` in your provided code, handles database operations)
├── requirements.txt
├── scraped_stock_data/
│   ├── sarbtm_news.csv
│   └── sarbtm_price_history.csv
└── README.md

a.py: Contains conceptual functions for scraping company profile, news, and price history data. In this setup, these functions are mocked to return predefined data, acting as placeholders for real web scraping. It also contains the main Streamlit application logic.

project.py (renamed from model.py in your provided code): Implements the machine learning model (predict_future_prices) for stock price prediction using Linear Regression.

model.py (renamed from mysql_db.py in your provided code): Handles database connectivity and operations (creating tables, inserting data) for MySQL using mysql.connector.

scraped_stock_data/: This directory is expected to contain the CSV files (sarbtm_news.csv and sarbtm_price_history.csv) with the mock or actual scraped data.

requirements.txt: Lists all the necessary Python dependencies.

README.md: This file.

Setup Instructions
Follow these steps to set up and run the project locally.

Prerequisites
Python 3.8+: Download and install from python.org.

XAMPP (or any MySQL server): For the database functionality. Download XAMPP from apachefriends.org.

Database Setup (XAMPP MySQL)
Start XAMPP: Open the XAMPP Control Panel and start the Apache and MySQL modules.

Access phpMyAdmin: Open your web browser and go to http://localhost/phpmyadmin.

Create Database:

Click on "New" in the left sidebar.

Enter sarbtm_db as the database name.

Click "Create".

Run Database Script:

Navigate to the model.py (originally mysql_db.py) file in your project directory.

Open a terminal or command prompt in your project's root directory.

Run the script to create tables and insert data:

python model.py

You should see "Data inserted into XAMPP MySQL successfully!" if everything worked.

Python Environment Setup
Clone the repository (if you haven't already):

git clone <repository_url>
cd <repository_name>

Create a virtual environment (recommended):

python -m venv venv

Activate the virtual environment:

On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

If requirements.txt is missing, create it with the following content:

streamlit
pandas
beautifulsoup4
requests
scikit-learn
mysql-connector-python
numpy

Then run pip install -r requirements.txt.

Running the Application
Ensure your virtual environment is activated.

Navigate to your project's root directory in the terminal.

Run the Streamlit application:

streamlit run a.py

Your browser will automatically open to the Streamlit app (usually http://localhost:8501).

Data Sources
The application primarily uses data loaded from local CSV files within the scraped_stock_data/ directory.

sarbtm_news.csv: Contains mock news data for SARBTM.

sarbtm_price_history.csv: Contains mock historical price data for SARBTM.

The functions in a.py are conceptual web scrapers and currently return mock data. To integrate real-time scraping, you would need to implement the actual scraping logic within get_company_profile_conceptual, get_company_news_conceptual, and get_sarabottam_price_history_conceptual, ensuring they parse the real sharesansar.com website.

Machine Learning Model
The project includes a basic Linear Regression model for predicting future stock prices.

File: project.py (originally model.py in your provided code).

Function: predict_future_prices(price_history_data, days_to_predict)

Methodology: It uses the 'close' prices from the historical data, converts dates into numerical "days since start" for the independent variable (X), and trains a LinearRegression model. Predictions are then made for the specified days_to_predict into the future.

Evaluation: The model's performance is evaluated using Mean Squared Error (MSE) and R-squared (R 
2
 ) metrics on the training data.

Important Note: Stock price prediction is highly complex. The linear regression model used here is a very simplistic approach and should not be used for real-world trading decisions. It serves as a demonstration of integrating a basic ML model. More sophisticated models, features, and data are required for accurate financial forecasting.

Customization
Company Symbol: To analyze a different company, change the COMPANY_SYMBOL variable in a.py. Remember to update or create corresponding NEWS_CSV_FILE and PRICE_HISTORY_CSV_FILE for the new symbol.

Scraping Logic: To scrape real data instead of using mock data, modify the get_company_profile_conceptual, get_company_news_conceptual, and get_sarabottam_price_history_conceptual functions in a.py to extract information directly from sharesansar.com or other relevant sources.

Prediction Model: For more advanced predictions, you can replace the LinearRegression model in project.py with other machine learning or deep learning models (e.g., ARIMA, LSTM).

Troubleshooting
mysql.connector.errors.ProgrammingError: 1045 (28000): Access denied for user 'root'@'localhost': This error usually means your MySQL root user has a password, but DB_CONFIG in model.py has an empty password. Update DB_CONFIG['password'] with your MySQL root password.

ModuleNotFoundError: Ensure you have installed all dependencies using pip install -r requirements.txt and activated your virtual environment.

CSV Files Not Found: Make sure sarbtm_news.csv and sarbtm_price_history.csv are present in the scraped_stock_data/ directory relative to where you run a.py.

Empty Dataframes in Streamlit: If the profile, news, or price history sections show "No data available," check the terminal where you launched Streamlit for any error messages from a.py or project.py during data loading. Also, verify the CSV file paths and content.

Contributing
Feel free to fork this repository, make improvements, and submit pull requests.

License
This project is open-source and available under the MIT License.
