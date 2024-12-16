# Project Structure

## `gui.py` - Main GUI Interface
- **`CreateGUI()`**: Constructs the graphical user interface (GUI) for the project.
  - **Control Elements**:
    - **Sliders**:
      - **LPC Order**: Adjusts the complexity of the Linear Predictive Coding model.
      - **Window Size**: Defines the amount of historical data used for predictions.
      - **Decay Factor**: Applies exponential decay to prioritize recent data.
    - **Buttons**:
      - **Start/Stop**: Control the simulation and real-time plotting.
      - **Save Data**: Exports raw and filtered stock price data to an Excel file.

## `plot.py` - Real-Time Plotting and Filtering
- **`fetch_stock_price()`**: Simulates real-time stock data using a Geometric Brownian Motion (GBM) model.
- **`set_smooth_ylim()`**: Dynamically adjusts the Y-axis for smooth transitions in the plot.
- **`apply_decay()`**: Applies an exponential decay factor to LPC coefficients to emphasize recent data trends.
- **`real_time_plot()`**: Handles real-time data processing and visualization.
  - Plots raw stock prices (blue) and LPC-filtered predictions (red).
  - Displays a predictive success rate and current decay factor in the plot title.

