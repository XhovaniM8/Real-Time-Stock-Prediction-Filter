# Project Structure

## `gui.py` - Main GUI Interface
- `CreateGUI()` - Creates the interface with controls
  - **Control Elements**:
    - Sliders for LPC order and window size
    - Start/Stop buttons
    - Save data button

## `plot.py` - Real-Time Plotting
- `fetch_stock_price()` - Simulates real-time stock data
- `set_smooth_ylim()` - Handles smooth Y-axis transitions
- `real_time_plot()` - Main plotting function
