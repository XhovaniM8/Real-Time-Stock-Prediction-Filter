import numpy as np
from analysis import arburg_vector
from stock_simulation import fetch_stock_price
import time

# Initialize a static variable to track time for stock price simulation
fetch_stock_price.t = 0

# Utility Functions
def set_smooth_ylim(ax, all_prices, margin=5):
    min_price, max_price = min(all_prices), max(all_prices)
    current_ylim = ax.get_ylim()
    target_ylim = (min_price - margin, max_price + margin)

    # Smoothly transition Y-axis limits
    new_ylim = (
        current_ylim[0] * 0.9 + target_ylim[0] * 0.1,
        current_ylim[1] * 0.9 + target_ylim[1] * 0.1,
    )
    ax.set_ylim(new_ylim)

def apply_decay(coeffs, decay_factor):
    decay_weights = np.exp(-decay_factor * np.arange(len(coeffs)))
    return coeffs * decay_weights


# Real-Time Plotting Function
def real_time_plot(lpc_order, window_size, decay_factor, fig, ax, canvas, plot_running, raw_prices, filtered_prices):
    success_count = 0
    total_predictions = 0
    margin_of_error = None  # Dynamically calculated during the run

    while plot_running():
        # Fetch the next stock price
        new_price = fetch_stock_price()
        raw_prices.append(new_price)

        # Dynamically calculate margin of error based on recent raw prices
        if len(raw_prices) > 1:
            margin_of_error = np.std(raw_prices[-window_size.get():]) * 0.5  # Half the recent volatility

        # Apply LPC filter if enough data points exist
        if len(raw_prices) >= lpc_order.get():
            try:
                coeffs, _, _ = arburg_vector(np.array(raw_prices), order=lpc_order.get())
                decayed_coeffs = apply_decay(coeffs, decay_factor.get())
                filtered_price = -np.dot(decayed_coeffs, raw_prices[-lpc_order.get():])
            except Exception as e:
                print(f"Error in LPC filtering: {e}")
                filtered_price = np.nan  # Handle LPC failures gracefully
            filtered_prices.append(filtered_price)

            # Check prediction success
            if not np.isnan(filtered_price) and len(raw_prices) > lpc_order.get():
                total_predictions += 1
                if abs(filtered_price - raw_prices[-1]) <= margin_of_error:
                    success_count += 1
        else:
            filtered_prices.append(new_price)

        # Calculate predictive success rate
        success_rate = (success_count / total_predictions * 100) if total_predictions > 0 else 0

        # Update the plot
        ax.clear()
        ax.plot(raw_prices, label="Raw Prices", color="blue")
        ax.plot(filtered_prices, label="Filtered Prices", color="red")
        ax.legend()

        # Add predictive success rate to the plot title
        ax.set_title(
            f"Stock Price with LPC Filtering\n"
            f"Predictive Success Rate: {success_rate:.2f}"
        )
        ax.set_xlabel("Time")
        ax.set_ylabel("Price")

        # Dynamically adjust Y-axis
        all_prices = [p for p in raw_prices + filtered_prices if not np.isnan(p)]  # Exclude NaNs
        if all_prices:
            set_smooth_ylim(ax, all_prices)

        # Redraw the canvas
        canvas.draw()

        # Sleep to maintain 30 FPS
        time.sleep(1 / 30)
