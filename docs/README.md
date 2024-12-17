# Real-Time Stock Price Prediction Filter

## Overview
This project demonstrates how Linear Predictive Coding (LPC) can be applied in real-time to predict stock price movements. The system simulates stock price data and allows dynamic control of LPC parameters via a user-friendly GUI.

## Features
- Real-time stock price simulation using Brownian motion.
- Predictive modeling with LPC filtering.
- Dynamic GUI with sliders to control:
  - LPC Order
  - Window Size
  - Decay Factor
- Predictive success rate and performance metrics displayed in real time.
  
## Requirements
- Python 3.8+
- Required dependencies (install via `requirements.txt`):

## Installation
1. Clone this repository:
 ```bash
 git clone https://github.com/your-username/real-time-stock-prediction-filter.git
 cd real-time-stock-prediction-filter
```

2. Set Up a Python Virtual Environment (Optional)

```bash
python3 -m venv .venv
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Run the Application

```bash
python src/main.py
```

# Project Structure

## Source Code (`src/`)
- `gui.py` - GUI interface and controls
- `plot.py` - Real-time plotting and LPC functionality  
- `analysis.py` - LPC coefficient calculation
- `stock_simulation.py` - Stock price simulation with GBM
- `synthesis.py` - Signal generation (LPC synthesis)
- `utils.py` - Utility functions like frequency response and cepstral conversions
- `main.py` - Main script to choose between GUI or testing modules
- `convert_to_excel.py` - Data saving to Excel
- `__init__.py` - Module initialization

## Documentation (`docs/`)
- `README.md` - Project overview and setup instructions
- `core_dsp_components.md` - Details on DSP processing
- `core_gui_components.md` - GUI structure and interactions

## Tests (`tests/`)
- `test_analysis.py` - Unit tests for analysis module
- `test_synthesis.py` - Unit tests for synthesis module
requirements.txt        # Dependencies for the project
.gitignore              # Git ignore file
