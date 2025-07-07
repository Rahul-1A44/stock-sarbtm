import streamlit as st
import pandas as pd
from a import ( 
    get_company_profile_conceptual,
)
from model import predict_future_prices
import time
import os 

COMPANY_SYMBOL = "SARBTM"
NEWS_CSV_FILE = os.path.join("scraped_stock_data", "sarbtm_news.csv")
PRICE_HISTORY_CSV_FILE = os.path.join("scraped_stock_data", "sarbtm_price_history.csv") 

st.set_page_config(
    page_title="NEPSE Stock Analyzer (SARBTM)",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #f0f2f5;
        color: #333;
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        background-image: linear-gradient(to right, #6366f1, #8b5cf6);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
    }
    .stAlert {
        border-radius: 8px;
        font-weight: 500;
    }
    h1, h2, h3 {
        color: #1a202c;
        font-weight: 700;
    }
    .section-header {
        border-bottom: 2px solid #edf2f7;
        padding-bottom: 0.75rem;
        margin-bottom: 1.5rem;
        font-size: 1.875rem; /* text-3xl */
    }
    .card-container {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 1.5rem;
        margin-bottom: 2rem;
    }
    .news-item {
        border-bottom: 1px dashed #e2e8f0;
        padding-bottom: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }
    .news-item:last-child {
        border-bottom: none;
        margin-bottom: 0;
        padding-bottom: 0;
    }
    .news-image {
        width: 100px; /* Fixed width for news image */
        height: 70px; /* Fixed height for news image */
        object-fit: cover;
        border-radius: 6px;
        flex-shrink: 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("NEPSE Stock Analyzer")
st.markdown(f"### Company: **Sarbottam Cement Limited ({COMPANY_SYMBOL})**")

st.sidebar.header("Data Control")
if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.session_state.clear() 
    st.rerun() 

if 'company_profile' not in st.session_state:
    with st.spinner('Loading company profile...'):
        profile_df = get_company_profile_conceptual(COMPANY_SYMBOL)
        st.session_state.company_profile = profile_df.iloc[0].to_dict() if not profile_df.empty else None
        if st.session_state.company_profile:
            st.info("Company profile loaded successfully.")
        else:
            st.warning("Failed to load company profile. Check terminal for errors from 'a.py'.")

if 'company_news' not in st.session_state:
    with st.spinner(f'Loading company news from {NEWS_CSV_FILE}...'):
        news_data = []
        if os.path.exists(NEWS_CSV_FILE):
            try:
                news_df = pd.read_csv(NEWS_CSV_FILE)
                if 'companySymbol' in news_df.columns:
                    news_df = news_df[news_df['companySymbol'] == COMPANY_SYMBOL]
                news_data = news_df.to_dict(orient='records')
                st.session_state.company_news = news_data
                st.info(f"Loaded {len(news_data)} news articles from {NEWS_CSV_FILE}.")
            except Exception as e:
                st.error(f"Error reading news from {NEWS_CSV_FILE}: {e}")
                st.session_state.company_news = []
        else:
            st.warning(f"News CSV file '{NEWS_CSV_FILE}' not found. Please ensure it's in the '{os.path.dirname(NEWS_CSV_FILE)}' directory.")
            st.session_state.company_news = []

if 'price_history' not in st.session_state:
    with st.spinner(f'Loading price history from {PRICE_HISTORY_CSV_FILE}...'):
        price_history_data = []
        if os.path.exists(PRICE_HISTORY_CSV_FILE):
            try:
                history_df = pd.read_csv(PRICE_HISTORY_CSV_FILE)
                if 'companySymbol' in history_df.columns:
                    history_df = history_df[history_df['companySymbol'] == COMPANY_SYMBOL]

                history_df = history_df.rename(columns={
                    'Date': 'date',
                    'Open': 'open',
                    'High': 'high',
                    'Low': 'low',
                    'Close': 'close',
                    'Volume': 'volume'
                })
                price_history_data = history_df.to_dict(orient='records')
                st.session_state.price_history = price_history_data
                st.info(f"Loaded {len(price_history_data)} price history entries from {PRICE_HISTORY_CSV_FILE}.")
            except Exception as e:
                st.error(f"Error reading price history from {PRICE_HISTORY_CSV_FILE}: {e}")
                st.session_state.price_history = []
        else:
            st.warning(f"Price History CSV file '{PRICE_HISTORY_CSV_FILE}' not found. Please ensure it's in the '{os.path.dirname(PRICE_HISTORY_CSV_FILE)}' directory.")
            st.session_state.price_history = []

company_profile = st.session_state.company_profile
news_data = st.session_state.company_news
price_history = st.session_state.price_history


st.header("Company Profile")
if company_profile:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Company Name:** {company_profile.get('companyName', 'N/A')}")
        st.write(f"**Symbol:** {company_profile.get('symbol', 'N/A')}")
        st.write(f"**Address:** {company_profile.get('address', 'N/A')}")
    with col2:
        st.write(f"**Sector:** {company_profile.get('sector', 'N/A')}")
        for key, value in company_profile.items():
            if key not in ['id', 'symbol', 'companyName', 'address', 'sector', 'lastUpdated']:
                st.write(f"**{key.replace('_', ' ').title()}:** {value}") 
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning(f"No company profile found for {COMPANY_SYMBOL}. Data might not be available or an error occurred during loading.")

st.header("Latest News")
if news_data:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    for news_item in news_data:
        st.markdown(f"""
            <div class="news-item">
                <img src="{news_item.get('news_image', 'https://placehold.co/150x100/A0A0A0/FFFFFF?text=No+Image')}" alt="News Image" class="news-image">
                <div>
                    <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 0.25rem;">{news_item.get('news_title', 'N/A')}</h3>
                    <p style="font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem;">{news_item.get('news_date', 'N/A')}</p>
                    <p style="font-size: 1rem; color: #4b5563;">{news_item.get('news_body', 'N/A')[:250]}...</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info(f"No news available for {COMPANY_SYMBOL}. Please ensure '{NEWS_CSV_FILE}' exists and contains data.")

st.header("Price History (Last 20 Days)")
if price_history:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    df_history = pd.DataFrame(price_history)
    st.dataframe(df_history, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info(f"No price history available for {COMPANY_SYMBOL}. Please ensure '{PRICE_HISTORY_CSV_FILE}' exists and contains data.")

st.header("Predicted Close Prices (Next 5 Days)")
if price_history and len(price_history) >= 10:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    predictions, ml_metrics = predict_future_prices(price_history)
    if predictions:
        st.subheader("Model Performance:")
        st.write(f"**Mean Squared Error (MSE):** {ml_metrics['MSE']:.2f}")
        st.write(f"**R-squared (R2):** {ml_metrics['R2']:.2f}")
        st.markdown("""
            <p style="font-size: 0.875rem; color: #6b7280; margin-top: 0.5rem;">
                *Note: Stock price prediction is complex. This model uses simple linear regression
                and may not be accurate for real-world trading. More data and advanced models
                are needed for better predictions.
            </p>
        """, unsafe_allow_html=True)

        st.subheader("Predictions:")
        df_predictions = pd.DataFrame(predictions)
        st.dataframe(df_predictions, use_container_width=True)
    else:
        st.warning("Could not generate predictions. Not enough historical data or an error occurred.")
    st.markdown('</div>', unsafe_allow_html=True)
elif price_history and len(price_history) < 10:
    st.warning(f"Not enough price history data ({len(price_history)} entries) to train the prediction model. Need at least 10 entries.")
else:
    st.info("No predictions available. Please ensure price history data is available.")
