#!/usr/local/bin/python3
# Plot Amdahl's Law

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(5, 5))
S = [0.0, 0.01, 0.02, 0.05, 0.1, 0.5]
nPoints = 14
legend = []
for j, s in enumerate(S):
    P = 1-s
    SpeedUp = np.ndarray(shape=(2, nPoints))
    Efficiency = np.ndarray(shape=(2, nPoints))

    for i in range(nPoints):
        N = pow(2, i*0.5)
        SpeedUp[0, i] = N
        SpeedUp[1, i] = 1/(s+P/N)
    plt.plot(SpeedUp[0, :], SpeedUp[1, :])
    legend.append("s = " '{:.2f}'.format(s))
    # plt.title("Amdahl's Law")
plt.legend(legend)
plt.ylabel("Speed up")
plt.xlabel("Number of CPUs")
plt.grid(True)
plt.ylim((1, N))
plt.xlim((1, N))
plt.show()

plt.figure(figsize=(5, 5))
for j, s in enumerate(S):
    P = 1-s
    SpeedUp = np.ndarray(shape=(2, nPoints))
    Efficiency = np.ndarray(shape=(2, nPoints))

    for i in range(nPoints):
        N = pow(2, i*0.5)
        SpeedUp[0, i] = N
        SpeedUp[1, i] = 1/(s+P/N)
        Efficiency[0, i] = N
        Efficiency[1, i] = 100*SpeedUp[1, i]/N
    plt.plot(Efficiency[0, :], Efficiency[1, :])
    legend.append("s = " '{:.2f}'.format(s))
#plt.title("Amdahl's Law")
plt.legend(legend)
plt.ylabel("Efficiency, %")
plt.xlabel("Number of CPUs")
plt.grid(True)
#plt.ylim((1, N))
plt.xlim((1, N))
plt.show()
