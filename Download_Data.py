import yfinance as yf
import sqlite3
import configparser

companies = ['AAPL', 'IBM', 'GOOGL', 'AMZN', 'MSFT']

# Connect to database
conn = sqlite3.connect('finance.db')
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS finance_data
             (company TEXT, date TEXT, open REAL, high REAL, low REAL, close REAL, volume INTEGER)''')

# Define the list of companies to download data for
with open('companies.txt') as file:
    companies = [line.strip() for line in file]

# Loop through companies and download data
for company in companies:
    print("Downloading data for",company,"company.....\n")
    ticker = yf.Ticker(company)
    data = ticker.history(period='max')
    for index, row in data.iterrows():
        cur.execute("INSERT OR REPLACE INTO finance_data VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (company, str(index.date()), row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

# Commit changes and close connection
conn.commit()
conn.close()

print("Download complete")
