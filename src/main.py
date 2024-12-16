import numpy as np
from analysis import arburg_vector, arburg_matrix
from synthesis import gen_ts
from utils import freqz, arcoeff_to_cep, cep_to_arcoeff
from gui import CreateGUI  # Import the GUI function to launch the application

np.seterr(invalid='ignore')  # Suppress numpy warnings


def test_analysis_module():
    """Test the functions in the analysis module."""
    print("Testing Analysis Module...")
    test_signal = np.sin(2 * np.pi * np.linspace(0, 1, 1000))
    lpc_order = 5
    coeffs, error, reflection = arburg_vector(test_signal, lpc_order)
    print(f"LPC Coefficients: {coeffs}")
    print(f"Error: {error}")
    print(f"Reflection Coefficients: {reflection}")


def test_synthesis_module():
    """Test the functions in the synthesis module."""
    print("Testing Synthesis Module...")
    coeffs = np.array([0.5, -0.3, 0.1])
    generated_signal = gen_ts(coeffs, sigma=0.1, n_samples=100)
    print(f"Generated Signal (first 10 samples): {generated_signal[:10]}")


def test_utils_module():
    """Test the functions in the utils module."""
    print("Testing Utils Module...")
    coeffs = np.array([0.5, -0.3, 0.1])
    sigma_squared = 0.01
    N = 10
    cep_coeffs = arcoeff_to_cep(coeffs, sigma_squared, N)
    recovered_coeffs = cep_to_arcoeff(cep_coeffs, len(coeffs))
    print(f"Cepstral Coefficients: {cep_coeffs}")
    print(f"Recovered LPC Coefficients: {recovered_coeffs}")
    freqs, power = freqz(coeffs, sigma_squared)
    print(f"Frequency Response: Frequencies (first 5): {freqs[:5]}, Power (first 5): {power[:5]}")


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Run Module Tests")
    print("2. Launch GUI")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == "1":
        print("Starting Module Tests...")
        print("-" * 50)
        test_analysis_module()
        print("-" * 50)
        test_synthesis_module()
        print("-" * 50)
        test_utils_module()
        print("All tests completed!")
    elif choice == "2":
        print("Launching GUI...")
        CreateGUI()
    else:
        print("Invalid choice. Exiting.")
