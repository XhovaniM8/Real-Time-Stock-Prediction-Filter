import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

def save_to_excel(raw_prices, filtered_prices, filename="stock_data.xlsx"):
    """Save stock prices and analytics to an Excel file.

    Parameters:
    ----------
    raw_prices : list
        The actual stock prices.
    filtered_prices : list
        The predicted stock prices.
    filename : str
        The name of the Excel file to save.
    """
    # Ensure raw and filtered lists are the same length
    min_len = min(len(raw_prices), len(filtered_prices))
    raw_prices = raw_prices[:min_len]
    filtered_prices = filtered_prices[:min_len]

    # Calculate analytics
    mse = mean_squared_error(raw_prices, filtered_prices)
    mae = mean_absolute_error(raw_prices, filtered_prices)
    correlation = np.corrcoef(raw_prices, filtered_prices)[0, 1]

    # Create a DataFrame
    data = {
        "Time": np.arange(min_len),
        "Raw Prices": raw_prices,
        "Filtered Prices": filtered_prices,
    }
    analytics = {
        "Metric": ["Mean Squared Error", "Mean Absolute Error", "Correlation"],
        "Value": [mse, mae, correlation],
    }

    df = pd.DataFrame(data)
    analytics_df = pd.DataFrame(analytics)

    # Write to Excel
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, index=False, sheet_name="Stock Data")
        analytics_df.to_excel(writer, index=False, sheet_name="Analytics")

    print(f"Data and analytics saved to {filename}")

# Example usage
if __name__ == "__main__":
    # Simulated example data
    raw_prices = [100, 102, 101, 103, 105]
    filtered_prices = [99, 101, 102, 104, 106]

    save_to_excel(raw_prices, filtered_prices)
