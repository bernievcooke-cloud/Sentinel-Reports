import matplotlib.pyplot as plt
import numpy as np
import datetime

# Create a new figure and set the size
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Generate sample data
x = np.linspace(0, 10, 100)

# First chart: Sine wave
axs[0].plot(x, np.sin(x), color='blue')
axs[0].set_title('Sine Wave')
axs[0].set_xlabel('X-axis')
axs[0].set_ylabel('Sin(X)')

# Second chart: Cosine wave
axs[1].plot(x, np.cos(x), color='red')
axs[1].set_title('Cosine Wave')
axs[1].set_xlabel('X-axis')
axs[1].set_ylabel('Cos(X)')

# Third chart: Tangent wave
axs[2].plot(x, np.tan(x), color='green')
axs[2].set_title('Tangent Wave')
axs[2].set_xlabel('X-axis')
axs[2].set_ylabel('Tan(X)')

# Adjust layout to prevent overlap
plt.tight_layout()

# Save the figure
plt.savefig('compact_surf_report.png')

# Show the figure
plt.show()