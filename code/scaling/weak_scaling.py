#!/usr/local/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def gustafson(ncpu, p):
    return ncpu-(1-p)*(ncpu-1)


data = np.loadtxt('weak_scaling.csv', delimiter=',')
# Sort data by number of CPUs
ind = np.argsort(data, axis=0)
data = data[ind[:, 0], :]
ncpu = data[:, 0]

# Initialize array for theoretical curves
tg = np.zeros(len(ncpu))

# Compute average computation time on 1 CPU
t1 = 0
c1 = 0
for x, y in data:
    if x == 1:
        t1 += y
        c1 += 1
    else:
        break
t1 /= c1

# Compute and plot speedup
speedup = t1*ncpu/data[:, 1]
plt.plot(ncpu, speedup, 'ok')

# Fit speedup with Amdahl's law
popt, pcov = curve_fit(gustafson, ncpu, speedup)

# Create optimized curve
for i, n in enumerate(ncpu):
    tg[i] = gustafson(n, popt)

# Plot measured and fitted curves
legend = []
legend.append("data")
legend.append("fit (s=" '{:.2f}'.format(float(1-popt))+")")
print("Serial fraction =", 1-popt)
plt.figure(1, figsize=(6, 6))
plt.plot(ncpu, tg, '--k')
plt.title("Weak Scaling")
plt.ylabel("Speed Up")
plt.xlabel("Number of CPUs")
plt.legend(legend)
plt.grid(True)
plt.savefig("weak_scaling.svg")
#plt.show()
