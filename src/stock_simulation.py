import numpy as np

# Parameters for Brownian Motion
s0 = 131.00          # Initial stock price
sigma = 0.25         # Volatility
mu = 0.35            # Drift (expected return)
delta = 1.0 / 252.0  # Time step (daily for 252 trading days in a year)
time = 252 * 5       # Simulation period (5 years)
paths = 1            # Number of paths for real-time simulation

# Geometric Brownian Motion Functions
def wiener_process(delta, sigma, time, paths):
    return sigma * np.random.normal(loc=0, scale=np.sqrt(delta), size=(time, paths))

def gbm_returns(delta, sigma, time, mu, paths):
    process = wiener_process(delta, sigma, time, paths)
    return np.exp(process + (mu - sigma**2 / 2) * delta)

def gbm_levels(s0, delta, sigma, time, mu, paths):
    returns = gbm_returns(delta, sigma, time, mu, paths)
    stacked = np.vstack([np.ones(paths), returns])
    return s0 * stacked.cumprod(axis=0)

# Precompute GBM Prices
gbm_prices = gbm_levels(s0, delta, sigma, time, mu, paths).flatten()  # Precompute GBM path
gbm_index = 0  # Initialize index for tracking GBM progression

def fetch_stock_price():
    global gbm_index
    if gbm_index < len(gbm_prices):
        price = gbm_prices[gbm_index]
        gbm_index += 1
        return price
    else:
        gbm_index = 0  # Restart the simulation if it reaches the end
        return gbm_prices[gbm_index]

# Test Function
if __name__ == "__main__":
    for _ in range(10):
        print(fetch_stock_price())
