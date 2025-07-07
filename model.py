import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import datetime
import os 

def predict_future_prices(price_history_data, days_to_predict=5):
    """
    Predicts future close prices using Linear Regression.

    Args:
        price_history_data (list of dict): A list of dictionaries, where each dictionary
                                           represents a day's price data. Expected keys:
                                           'date' (str YYYY-MM-DD), 'close' (float).
                                           Note: The function expects 'close' for the actual
                                           prediction, but the sample data uses 'close_price'.
                                           Ensure consistency or adapt.
        days_to_predict (int): The number of future days to predict.

    Returns:
        tuple: A tuple containing:
            - predictions_output (list of dict): Predicted dates and close prices.
            - metrics (dict): MSE and R2 score of the model on training data.
    """
    if not price_history_data:
        print("No price history data provided for prediction.")
        return [], None
    df = pd.DataFrame(price_history_data)
    if 'close' not in df.columns:
        print("Error: 'close' column not found in price history data. Cannot predict.")
        return [], None

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').reset_index(drop=True)
    df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
    X = df[['days_since_start']]
    y = df['close'] 

    model = LinearRegression()
    model.fit(X, y) 
    y_pred_train = model.predict(X)
    mse = mean_squared_error(y, y_pred_train)
    r2 = r2_score(y, y_pred_train)
    metrics = {"MSE": mse, "R2": r2}
    print(f"Model Training Metrics: MSE={mse:.2f}, R2={r2:.2f}")
    last_known_date = df['date'].max()
    future_dates = [last_known_date + datetime.timedelta(days=i) for i in range(1, days_to_predict + 1)]
    future_days_since_start = [(d - df['date'].min()).days for d in future_dates]
    X_future = pd.DataFrame({'days_since_start': future_days_since_start})
    predicted_prices = model.predict(X_future)
    predictions_output = []
    for i, date in enumerate(future_dates):
        predictions_output.append({
            'date': date.strftime('%Y-%m-%d'),
            'predicted_close_price': round(float(predicted_prices[i]), 2)
        })

    return predictions_output, metrics

if __name__ == "__main__":
    print("\n--- Testing ML Model with sarbtm_price_history.csv ---")
    PRICE_HISTORY_CSV_FILE = os.path.join("scraped_stock_data", "sarbtm_price_history.csv")

    if os.path.exists(PRICE_HISTORY_CSV_FILE):
        try:
            df_from_csv = pd.read_csv(PRICE_HISTORY_CSV_FILE)
            df_from_csv = df_from_csv.rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close', 
                'Volume': 'volume'
            })
            price_history_for_model = df_from_csv.to_dict(orient='records')

            predictions, metrics = predict_future_prices(price_history_for_model, days_to_predict=5)

            if predictions:
                print("\nPredicted Close Prices for next 5 days:")
                for pred in predictions:
                    print(f"  Date: {pred['date']}, Predicted Price: {pred['predicted_close_price']}")
            else:
                print("Could not generate predictions.")

            if metrics:
                print(f"\nModel Evaluation Metrics: MSE={metrics['MSE']:.2f}, R2={metrics['R2']:.2f}")

        except Exception as e:
            print(f"Error loading or processing CSV for model testing: {e}")
    else:
        print(f"Error: CSV file not found at '{PRICE_HISTORY_CSV_FILE}'. Cannot test model.")

