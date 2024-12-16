import numpy as np

# Setup params for Brownian motion
s0 = 131.00
sigma = 0.25
mu = 0.35
delta = 1.0 / 252.0  # Time step (daily for 252 trading days in a year)
time = 252 * 5       # Simulate for 5 years
paths = 1            # Single path for real-time simulation

# Define the Wiener process
def wiener_process(delta, sigma, time, paths):
    """Returns a Wiener process."""
    return sigma * np.random.normal(loc=0, scale=np.sqrt(delta), size=(time, paths))

# Define GBM returns
def gbm_returns(delta, sigma, time, mu, paths):
    """Returns from a Geometric Brownian motion."""
    process = wiener_process(delta, sigma, time, paths)
    return np.exp(process + (mu - sigma ** 2 / 2) * delta)

# Define GBM levels
def gbm_levels(s0, delta, sigma, time, mu, paths):
    """Returns price paths starting at s0."""
    returns = gbm_returns(delta, sigma, time, mu, paths)
    stacked = np.vstack([np.ones(paths), returns])
    return s0 * stacked.cumprod(axis=0)

# Precompute GBM prices
gbm_prices = gbm_levels(s0, delta, sigma, time, mu, paths).flatten()  # Precompute GBM path
gbm_index = 0  # Initialize index for tracking GBM progression

# Fetch the next price
def fetch_stock_price():
    """Fetch the next price from the precomputed GBM prices."""
    global gbm_index
    if gbm_index < len(gbm_prices):
        price = gbm_prices[gbm_index]
        gbm_index += 1
        return price
    else:
        gbm_index = 0  # Restart the simulation if it reaches the end
        return gbm_prices[gbm_index]

# Test the function
if __name__ == "__main__":
    for _ in range(10):
        print(fetch_stock_price())
