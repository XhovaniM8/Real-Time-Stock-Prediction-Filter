import numpy as np
from scipy import signal as sig

def arcoeff_to_cep(a, sigma_squared, N):
    """
    Calculate Cepstral Coefficients from LPC (Linear Predictive Coding) coefficients.

    Parameters:
    - a (numpy.ndarray): LPC coefficients [a1, a2, ...] (without the leading 1).
    - sigma_squared (float): Square of noise power.
    - N (int): Desired length of cepstrum coefficients.

    Returns:
    - numpy.ndarray: First N cepstral coefficients (c0, c1, ..., cN-1) where c0 = log(sigma^2).
    """
    c = [0] * N
    c[0] = np.log(sigma_squared)
    c[1] = -a[0]
    for n in range(2, N):
        if n <= len(a):
            c[n] = -a[n - 1] - sum((1 - m / n) * a[m - 1] * c[n - m] for m in range(1, n))
        else:
            c[n] = -sum((1 - m / n) * a[m - 1] * c[n - m] for m in range(1, len(a) + 1))
    return c

def cep_to_arcoeff(c, order):
    """
    Calculate LPC (Linear Predictive Coding) coefficients from Cepstral Coefficients.

    Parameters:
    - c (numpy.ndarray): Cepstrum coefficients [c0, c1, ...] where c0 = log(sigma^2).
    - order (int): Order of the LPC model.

    Returns:
    - numpy.ndarray: LPC coefficients [a1, a2, ...] (without the leading 1).
    """
    a = [0] * order
    a[0] = -c[1]
    for i in range(2, order + 1):
        a[i - 1] = -c[i] - sum((1 - m / i) * c[i - m] * a[m - 1] for m in range(1, i))
    return a

def freqz(a=1, sigma_squared=1, worN=1000, whole=False, fs=500):
    """
    Calculate the power spectrum from LPC coefficients.

    Parameters:
    - a (numpy.ndarray): LPC coefficients [a1, a2, ...] (without the leading 1). Default is 1.
    - sigma_squared (float): Square of noise power. Default is 1.
    - worN (int): Number of points for the frequency response computation. Default is 1000.
    - whole (bool): Frequency range (0 to π if False, 0 to Nyquist if True). Default is False.
    - fs (float): Sampling frequency in Hz. Default is 500.

    Returns:
    - numpy.ndarray: Array of frequencies in Hz.
    - numpy.ndarray: Power at each frequency in dB.
    """
    a = np.insert(a, 0, 1)
    b = np.zeros_like(a)
    b[0] = 1
    w, h = sig.freqz(b, a, worN=worN, whole=whole, fs=fs)
    pwr = 20 * np.log10(abs(h) * np.sqrt(sigma_squared))
    return w, pwr

def arcoeff_warp(a, warp_factor, task="warp"):
    """
    Recalculate LPC coefficients with frequency warping or unwarping.

    Parameters:
    - a (numpy.ndarray): LPC coefficients [a1, a2, ...] (without the leading 1).
    - warp_factor (float): Frequency warping factor (-1 to 1).
    - task (str): Objective of the function ("warp" or "unwarp").

    Returns:
    - numpy.ndarray: Warped or unwarped LPC coefficients [a1, a2, ...] (without the leading 1).
    """
    if task == "warp":
        s = -1
    elif task == "unwarp":
        s = 1
    else:
        raise ValueError("task must be 'warp' or 'unwarp'")

    a = np.insert(a, 0, 1)
    b = np.zeros_like(a)
    b[0] = 1

    # Get poles
    z, p, k = sig.tf2zpk(b, a)

    # Pole conversion
    p_new = (p + s * warp_factor) / (1 + s * warp_factor * p)

    # Convert back to LPC coefficients
    b, a = sig.zpk2tf(z, p_new, k)
    return a[1:]  # Exclude the leading 1
