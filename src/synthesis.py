import numpy as np
from scipy.signal import lfilter


def gen_ts(a, sigma=1, n_samples=1000, data=None):
    """
    Generate a time series using LPC coefficients.

    Parameters:
    - a (numpy.ndarray): LPC coefficients [a1, a2, ...] (without the leading 1).
    - sigma (float): Noise power. Defaults to 1.
    - n_samples (int): Total number of generated samples. Defaults to 1000.
    - data (numpy.ndarray): Input time series data. If provided, 'sigma' and 'n_samples' are ignored. Defaults to None.

    Returns:
    - numpy.ndarray: Generated time series.
      Shape: (1, n_samples) or the same shape as 'data'.
    """
    if data is None:
        mean = 0
        std_dev = sigma
        data = np.random.normal(mean, std_dev, n_samples)

    # Generate time series using LPC coefficients
    time_series = lfilter([1], np.hstack(([1], a)), data)

    # Ensure the output is real-valued
    time_series = np.real(time_series)

    return time_series
