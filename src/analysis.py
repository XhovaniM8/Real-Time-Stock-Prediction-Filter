import numpy as np


# --------------------------------------------------------------
# LPC (Linear Predictive Coding) Analysis Functions
# --------------------------------------------------------------

def arburg_vector(x, order=1):
    """
    Calculates LPC coefficients from time series data.

    Parameters:
        x (numpy.ndarray): Vector of time series data.
        order (int): LPC order. Must be > 0.

    Returns:
        tuple: LPC coefficients (a), error power (E), and reflection coefficients (ref).
    """
    x = np.array(x)
    N = len(x)

    if order <= 0:
        raise ValueError("Order must be > 0")

    # Initialization
    efp = x[1:]
    ebp = x[:-1]
    E = np.dot(x, x) / N  # Initial error
    a = np.zeros(order + 1)
    a[0] = 1
    ref = np.zeros(order)
    epsilon = 1e-10  # Small constant to avoid division by zero

    for m in range(order):
        # Calculate reflection (parcor) coefficient
        denominator = np.dot(efp.T, efp) + np.dot(ebp, ebp)
        k = (-2 * np.dot(ebp, efp)) / (denominator + epsilon) if denominator != 0 else 0
        ref[m] = k

        # Update forward and backward prediction errors
        ef = efp[1:] + k * ebp[1:]
        ebp = ebp[:-1] + np.conj(k) * efp[:-1]
        efp = ef

        # Update AR coefficients
        if m == 0:
            a[1] = a[1] + k * np.conj(a[0])
        else:
            a[1:m + 2] = a[1:m + 2] + k * np.conj(a[m::-1])

        # Update prediction error
        E = (1 - np.conj(k) * k) * E

    return a[1:], E, ref


def arburg_matrix(X, order=1):
    """
    Calculates LPC coefficients for multiple time series data.

    Parameters:
        X (numpy.ndarray): Matrix of time series data. Shape: n x obs.
        order (int): LPC order. Must be > 0.

    Returns:
        tuple: LPC coefficient matrix (a), error power (E), and reflection coefficients (ref).
    """
    x = np.array(X)
    N, obs = x.shape

    if order <= 0:
        raise ValueError("Order must be > 0")

    # Initialization
    efp = x[1:, :]
    ebp = x[:-1, :]
    E = np.einsum('ij,ij->j', x, x) / N  # Efficient computation of initial error
    a = np.zeros((order + 1, obs))
    a[0, :] = 1
    ref = np.zeros((order, obs))

    for m in range(order):
        # Calculate reflection coefficients
        k = (-2 * np.einsum('ij,ij->j', ebp, efp)) / (
                np.einsum('ij,ij->j', efp, efp) + np.einsum('ij,ij->j', ebp, ebp)
        )
        ref[m, :] = k

        # Update forward and backward prediction errors
        ef = efp[1:, :] + k * ebp[1:, :]
        ebp = ebp[:-1, :] + np.conj(k) * efp[:-1, :]
        efp = ef

        # Update AR coefficients
        if m == 0:
            a[1, :] = a[1, :] + k * np.conj(a[0, :])
        else:
            a[1:m + 2, :] = a[1:m + 2, :] + k * np.conj(a[m::-1, :])

        # Update prediction error
        E = (1 - np.conj(k) * k) * E

    return a[1:, :], E, ref


# --------------------------------------------------------------
# Frequency-Warped LPC Functions
# --------------------------------------------------------------

def arburg_warped_vector(x, order=1, warp_factor=0):
    """
    Calculates frequency-warped LPC coefficients from time series data.
    """
    N = len(x)
    E = np.dot(x, x) / N
    ref = np.zeros(order)
    ebp = x.copy()
    efp = x.copy()

    for index in range(1, order + 1):
        bb = np.zeros(N - index)
        bb[0] = ebp[0] - warp_factor * ebp[1]
        for i in range(1, N - index):
            bb[i] = ebp[i] - warp_factor * (ebp[i + 1] - bb[i - 1])
        F = efp[1:]
        k = (-2 * np.dot(F.T, bb)) / (np.dot(F.T, F) + np.dot(bb.T, bb))
        ref[index - 1] = k
        efp = F + k * bb
        ebp = bb + k * F
        E = (1 - np.conj(k) * k) * E

    # Calculate LPC coefficients
    a = np.array([1])
    for index in range(order):
        aa = np.concatenate((a, [0]))
        J = np.eye(len(aa))[::-1]
        a = aa + ref[index]
