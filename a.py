import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import datetime
import streamlit as st 

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive',
}

@st.cache_data(ttl=3600, show_spinner=False) 
def get_company_profile_conceptual(company_symbol="SARBTM"):
    print(f"\nAttempting to conceptually scrape profile for {company_symbol}...")
    url = f"https://www.sharesansar.com/company/{company_symbol.lower()}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10) 
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        profile_data = {
            'symbol': company_symbol,
            'companyName': f"{company_symbol} Company Ltd. (Mock)",
            'sector': "Manufacturing And Processing (Mock)",
            'sharesOutstanding': 49755000.00,
            'marketPrice': 861.88,
            'changePercentage': 1.58,
            'lastTradedOn': "2025/07/06",
            'fiftyTwoWeekHighLow': "1,060.00-696.80",
            'eps': 16.16,
            'peRatio': 53.33,
            'bookValue': 193.93,
            'pbv': 4.44,
            'dividendPercentage': 3.00,
            'address': "Mock Address, Kathmandu, Nepal",
            'website': "mock-company.com",
            'phone': "+977 01 XXXXXXX",
            'email': "info@mockcompany.com",
            'lastUpdated': datetime.datetime.now().isoformat()
        }
        df = pd.DataFrame([profile_data])
        print(f"Conceptually scraped profile for {company_symbol}.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching company profile for {company_symbol}: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while processing company profile for {company_symbol}: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_company_news_conceptual(company_symbol="SARBTM", num_news=2):
    print(f"\nAttempting to scrape news for {company_symbol}...")
    url = f"https://www.sharesansar.com/company/{company_symbol.lower()}/news"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        news_data = []
        today = datetime.date.today()
        news_data.append({
            'companySymbol': company_symbol,
            'news_title': "Bonus Shares of Mero Microfinance and Sarbottam Cement Now Listed in NEPSE",
            'news_date': (today - datetime.timedelta(days=10)).isoformat(),
            'news_url': "https://www.sharesansar.com/newsdetail/bonus-shares-of-mero-microfinance-and-sarbottam-cement-now-listed-in-nepse-2025-03-24",
            'news_body': "This is a mock news body for the first article. The company announced impressive financial results for the first quarter, exceeding analyst expectations. Revenue grew by 15% year-over-year, driven by strong sales in key markets. The CEO expressed optimism about future growth prospects."
        })
        news_data.append({
            'companySymbol': company_symbol,
            'news_title': "Mock News: New Product Launch Announced",
            'news_date': (today - datetime.timedelta(days=25)).isoformat(),
            'news_url': "https://www.sharesansar.com/newsdetail/sarbottam-cements-net-profit-soars-by-68923-in-q1-revenue-grows-nearly-36-eps-at-rs-970-2025-02-11",
            'news_body': "This is a mock news body for the second article. The company has officially unveiled its latest product line, promising innovative features and enhanced user experience. Pre-orders have already surpassed initial targets, indicating strong market demand. Production is expected to scale up in the coming months."
        })
        df = pd.DataFrame(news_data)
        print(f"Conceptually scraped {len(news_data)} news articles for {company_symbol}.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching company news for {company_symbol}: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while processing company news for {company_symbol}: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)

def get_sarabottam_price_history_conceptual(company_symbol="SARBTM", num_days=20):
    """
    Conceptual function to scrape price history.
    You need to replace the mock data with actual scraping logic.
    """
    print(f"\nAttempting to conceptually scrape price history for {company_symbol}...")
    url = f"https://www.sharesansar.com/company/{company_symbol.lower()}/price-history"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10) 
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')



        mock_data = []
        today = datetime.date.today()
        for i in range(num_days):
            date = today - datetime.timedelta(days=i)
            mock_data.append({
                'companySymbol': company_symbol,
                'date': date.isoformat(),
                'open': round(850 + i * 0.5 + (datetime.datetime.now().microsecond % 1000) / 1000 * 5, 2),
                'high': round(860 + i * 0.5 + (datetime.datetime.now().microsecond % 1000) / 1000 * 5, 2),
                'low': round(840 + i * 0.5 - (datetime.datetime.now().microsecond % 1000) / 1000 * 5, 2),
                'close': round(855 + i * 0.5 + (datetime.datetime.now().microsecond % 1000) / 1000 * 5, 2),
                'volume': int(10000 + i * 100 + (datetime.datetime.now().microsecond % 1000) / 1000 * 500)
            })
        df = pd.DataFrame(mock_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=False).head(num_days).reset_index(drop=True)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        print(f"Conceptually scraped {len(df)} days of price history for {company_symbol}.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching price history for {company_symbol}: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while processing price history for {company_symbol}: {e}")
        return pd.DataFrame()
