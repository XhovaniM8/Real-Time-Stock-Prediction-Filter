import numpy as np
import matplotlib.pyplot as plt
from analysis import arburg_vector
from stock_simulation import fetch_stock_price
import time

# Initialize a static variable to track time for stock price simulation
fetch_stock_price.t = 0

# --------------------------------------------------------------
# Utility Functions
# --------------------------------------------------------------

def set_smooth_ylim(ax, all_prices, margin=5):
    """
    Dynamically adjust Y-axis limits with a margin to reduce plot jumping.

    Parameters:
        ax (matplotlib.axes.Axes): The axis object to modify.
        all_prices (list): Combined list of raw and filtered prices.
        margin (float): Margin to add above and below the data range.
    """
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
    """
    Applies exponential decay to LPC coefficients.

    Parameters:
        coeffs (np.ndarray): The LPC coefficients.
        decay_factor (float): The decay factor (0 to 1). Higher values retain more weight on older coefficients.

    Returns:
        np.ndarray: The decayed LPC coefficients.
    """
    decay_weights = np.exp(-decay_factor * np.arange(len(coeffs)))
    return coeffs * decay_weights

# --------------------------------------------------------------
# Real-Time Plotting Function
# --------------------------------------------------------------

def real_time_plot(lpc_order, window_size, decay_factor, fig, ax, canvas, plot_running, raw_prices, filtered_prices):
    """
    Plot the stock price data in real-time alongside LPC-filtered predictions with a decay factor.

    Parameters:
        lpc_order (tk.IntVar): Variable controlling the LPC order.
        window_size (tk.IntVar): Variable controlling the window size for LPC.
        decay_factor (tk.DoubleVar): Variable controlling the exponential decay factor.
        fig (matplotlib.figure.Figure): The figure object for plotting.
        ax (matplotlib.axes.Axes): The axis object for plotting.
        canvas (FigureCanvasTkAgg): The canvas to draw the plot.
        plot_running (function): Callback to check if the plot should keep running.
        raw_prices (list): List to store raw stock prices.
        filtered_prices (list): List to store LPC-filtered prices.
    """
    success_count = 0
    total_predictions = 0
    margin_of_error = None  # Dynamically calculated during the run

    while plot_running():
        # Fetch the next stock price
        new_price = fetch_stock_price()
        raw_prices.append(new_price)

        # Dynamically calculate margin of error based on recent raw prices
        if len(raw_prices) > 1:
            margin_of_error = np.std(raw_prices[-window_size.get():]) * 0.5  # Example: Half the recent volatility

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
            f"Full Stock Price Climb with LPC Filtering\n"
            f"Predictive Success Rate: {success_rate:.2f}% | Decay Factor: {decay_factor.get():.2f}"
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

# --------------------------------------------------------------
# Notes
# --------------------------------------------------------------
# - `fetch_stock_price`: Simulates stock price data in real-time.
# - `arburg_vector`: Performs LPC analysis to predict the next price.
# - `apply_decay`: Applies an exponential decay factor to prioritize recent coefficients.
# - `real_time_plot`: Combines raw prices, filtered LPC predictions, and predictive success rate with decay factor.
# - Decay factor allows fine-tuning of the prediction model's sensitivity to recent trends.
