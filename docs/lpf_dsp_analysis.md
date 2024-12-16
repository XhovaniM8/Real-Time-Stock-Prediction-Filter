# Step-by-Step Math for LPC Coefficients (Burg Method)

## Step 1: Problem Setup

LPC models a signal \( x[n] \) as a linear combination of its past values:

\[
x[n] \approx -a_1 x[n-1] - a_2 x[n-2] - \dots - a_p x[n-p]
\]

Where:
- \( x[n] \) is the current signal sample.
- \( a_1, a_2, \dots, a_p \) are the LPC coefficients.
- \( p \) is the order of the LPC model.

The goal is to find \( \{a_1, a_2, \dots, a_p\} \) that minimizes the prediction error energy \( E \), defined as:

\[
E = \sum_{n=p}^{N-1} \left( x[n] + \sum_{k=1}^p a_k x[n-k] \right)^2
\]

---

## Step 2: Initialize Burg Method

1. **Initial Error**:
   \[
   E_0 = \frac{1}{N} \sum_{n=0}^{N-1} x[n]^2
   \]

   This is the total energy of the signal.

2. **Initial Forward and Backward Prediction Errors**:
   - Forward error: \( f[n] = x[n] \)
   - Backward error: \( b[n] = x[n] \)

---

## Step 3: Iterative Calculation of LPC Coefficients

For each order \( m \) (from 1 to \( p \)):

### 1. Calculate the Reflection Coefficient:
\[
k_m = -2 \cdot \frac{\sum_{n=m}^{N-1} f[n] b[n-1]}{\sum_{n=m}^{N-1} f[n]^2 + \sum_{n=m-1}^{N-2} b[n]^2}
\]

Where:
- \( f[n] \): forward prediction error.
- \( b[n] \): backward prediction error.

---

### 2. Update the LPC Coefficients:
The new coefficient is:
\[
a_m^{(m)} = k_m
\]

Update previous coefficients:
\[
a_k^{(m)} = a_k^{(m-1)} + k_m \cdot a_{m-k}^{(m-1)}, \quad \text{for } k = 1, \dots, m-1
\]

---

### 3. Update the Prediction Errors:
\[
f[n] = f[n] + k_m \cdot b[n-1]
\]
\[
b[n] = b[n-1] + k_m \cdot f[n]
\]

---

### 4. Update Total Error:
\[
E_m = E_{m-1} \cdot (1 - k_m^2)
\]

---

## Step 4: Final Coefficients

After \( p \) iterations, the coefficients \( \{a_1, a_2, \dots, a_p\} \) are the final LPC coefficients for the signal.

---

## Example Calculation

Given the signal: \( x = [1, -1, 2, -2, 3] \), \( N = 5 \), and \( p = 2 \):

1. **Initialize**:
   - Compute initial error:
     \[
     E_0 = \frac{1}{5} (1^2 + (-1)^2 + 2^2 + (-2)^2 + 3^2) = 4.2
     \]
   - Forward and backward errors are initialized to \( x[n] \).

2. **First Iteration (Order 1)**:
   - Calculate \( k_1 \):
     \[
     k_1 = -2 \cdot \frac{\sum_{n=1}^{4} f[n] b[n-1]}{\sum_{n=1}^{4} f[n]^2 + \sum_{n=0}^{3} b[n]^2}
     \]
   - Substitute values of \( f[n] \) and \( b[n] \) to compute \( k_1 \).
   - Update:
     - \( a_1 \)
     - Forward and backward errors.
     - Total error \( E_1 \).

3. **Second Iteration (Order 2)**:
   - Calculate \( k_2 \):
     \[
     k_2 = -2 \cdot \frac{\sum_{n=2}^{4} f[n] b[n-1]}{\sum_{n=2}^{4} f[n]^2 + \sum_{n=1}^{3} b[n]^2}
     \]
   - Update:
     - \( a_1, a_2 \)
     - Forward and backward errors.
     - Total error \( E_2 \).

---

## Key Notes

- Perform these calculations iteratively for \( p \) orders.
- Each reflection coefficient \( k_m \) represents the current order’s contribution.
- The LPC coefficients are normalized to ensure minimal prediction error.

---
