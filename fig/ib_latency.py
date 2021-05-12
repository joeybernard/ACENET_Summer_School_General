#!/usr/local/bin/python3
# Infiniband latency data from
# DOI: 10.5815/ijcnis.2016.10.02

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('latency.csv', delimiter=' ')
plt.plot(data[:, 0], data[:, 1], '-ok')
plt.title("Infiniband latency (DOI: 0.5815/ijcnis.2016.10.02)")
plt.ylabel("Latency, microseconds")
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Message size, bytes")
plt.grid(True)
plt.show()
