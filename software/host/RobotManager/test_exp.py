import numpy as np
import matplotlib.pyplot as plt

def map_input(x, factor=10.0):
    """
    Maps input x in [0,1] to another value in [0,1] using an exponential curve.
    """
    sign = np.sign(x)
    return sign*(np.exp(x * np.log(factor)) - 1) / (factor - 1)

def log_map(x, base=10):
    """
    Maps input x in [0,1] to another value in [0,1] using a logarithmic curve.
    """
    return np.log1p(x * (base - 1)) / np.log(base)

# Generate x values from 0 to 1
x_values = np.linspace(0, 1, 100)

# Compute y values for both functions
y_exp = log_exp_map(x_values, factor=10)  # Change factor to adjust curve
y_log = log_map(x_values, base=10)       # Change base to adjust curve

# Plot the functions
plt.figure(figsize=(8, 6))
plt.plot(x_values, x_values, '--', label="Identity (y=x)", color='gray')
plt.plot(x_values, y_exp, label="Exponential Mapping (factor=4)", color='blue')
plt.plot(x_values, y_log, label="Logarithmic Mapping (base=10)", color='red')

# Labels and title
plt.xlabel("Input x")
plt.ylabel("Transformed Value")
plt.title("Comparison of Logarithmic and Exponential Mappings")
plt.legend()
plt.grid(True)

# Show plot
plt.show()
