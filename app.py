from flask import Flask, render_template, request, redirect, url_for
import os
from a import scrape_sarbottam_cement_data
import _mysql_connector
from ml_model import predict_future_prices

app = Flask(__name__)

COMPANY_SYMBOL = "SARBTM"

@app.route('/')
def index():
    company_profile = get_company_profile(COMPANY_SYMBOL)
    news_data = get_news_data(COMPANY_SYMBOL)
    price_history = get_price_history(COMPANY_SYMBOL)

    predictions = []
    ml_metrics = None
    if price_history:
        predictions, ml_metrics = predict_future_prices(price_history)

    return render_template(
        'index.html',
        company_profile=company_profile,
        news_data=news_data,
        price_history=price_history,
        predictions=predictions,
        ml_metrics=ml_metrics,
        company_symbol=COMPANY_SYMBOL
    )

@app.route('/scrape_and_save')
def scrape_and_save_data():
    """
    Triggers the scraping process and saves data to Firestore.
    Redirects back to the index page after completion.
    """
    print(f"Initiating scrape for {COMPANY_SYMBOL}...")
    profile, news, history = scrape_sarbottam_cement_data()

    if profile:
        save_company_profile(profile)
    if news:
        save_news_data(COMPANY_SYMBOL, news)
    if history:
        save_price_history(COMPANY_SYMBOL, history)

    print("Scraping and saving process completed.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('serviceAccountKey.json'):
        print("ERROR: 'serviceAccountKey.json' not found in the project root.")
        print("Please download it from your Firebase project settings > Service accounts.")
        exit()

    app.run(debug=True) 
