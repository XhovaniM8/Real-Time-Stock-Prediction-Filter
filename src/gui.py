import tkinter as tk
from tkinter import IntVar, DoubleVar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
from plot import real_time_plot  # Import the plotting function
from convert_to_excel import save_to_excel  # Import the save function (Not currently functioning)

# Global variables
plot_running = False  # Flag to control the plotting thread
raw_prices = []  # List to store raw prices
filtered_prices = []  # List to store filtered prices


def CreateGUI():
    """Create the main GUI for real-time stock price prediction."""
    global plot_running

    # Initialize the main window
    root = tk.Tk()
    root.title("Real-Time Stock Price Prediction Filter")

    # Control Frame (Left Panel)
    control_frame = tk.Frame(root)
    control_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)

    # SLIDERS BEGIN

    # LPC Order Slider
    tk.Label(control_frame, text="LPC Order").grid(row=0, column=0, columnspan=2, pady=5)
    lpc_order = IntVar(value=10)
    tk.Scale(
        control_frame, from_=1, to=20, orient="horizontal", variable=lpc_order,
        command=lambda _: slider_changed()
    ).grid(row=1, column=0, columnspan=2, pady=5)

    # Window Size Slider
    tk.Label(control_frame, text="Window Size").grid(row=2, column=0, columnspan=2, pady=5)
    window_size = IntVar(value=50)
    tk.Scale(
        control_frame, from_=10, to=200, orient="horizontal", variable=window_size,
        command=lambda _: slider_changed()
    ).grid(row=3, column=0, columnspan=2, pady=5)

    # Decay Factor Slider
    tk.Label(control_frame, text="Decay Factor").grid(row=4, column=0, columnspan=2, pady=5)
    decay_factor = DoubleVar(value=0.1)
    tk.Scale(
        control_frame, from_=0.01, to=1.0, resolution=0.01, orient="horizontal", variable=decay_factor,
        command=lambda _: slider_changed()
    ).grid(row=5, column=0, columnspan=2, pady=5)

    # SLIDERS END

    # Plot Frame (Right Panel)
    plot_frame = tk.Frame(root)
    plot_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    fig, ax = plt.subplots(figsize=(8, 4))
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Start Plotting
    def start_plot():
        global plot_running, raw_prices, filtered_prices
        if not plot_running:
            plot_running = True
            if not raw_prices:  # Clear prices only if the thread is not running
                raw_prices.clear()
                filtered_prices.clear()
            threading.Thread(
                target=real_time_plot,
                args=(lpc_order, window_size, decay_factor, fig, ax, canvas, lambda: plot_running, raw_prices, filtered_prices),
                daemon=True
            ).start()

    # Stop Plotting
    def stop_plot():
        global plot_running
        plot_running = False

    # Save Data to Excel
    def save_data():
        if raw_prices and filtered_prices:
            save_to_excel(raw_prices, filtered_prices, "stock_analysis.xlsx")
            print("Data saved to 'stock_analysis.xlsx'")
        else:
            print("No data to save. Please start and stop the plot first.")

    # Control Buttons
    tk.Button(control_frame, text="Start Plotting", command=start_plot).grid(row=6, column=0, columnspan=2, pady=5)
    tk.Button(control_frame, text="Stop Plotting", command=stop_plot).grid(row=7, column=0, columnspan=2, pady=5)
    # tk.Button(control_frame, text="Save Data to Excel", command=save_data).grid(row=8, column=0, columnspan=2, pady=5)

    # Slider Change Handler
    def slider_changed():
        """Stop the plot when sliders are adjusted."""
        stop_plot()

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    CreateGUI()
