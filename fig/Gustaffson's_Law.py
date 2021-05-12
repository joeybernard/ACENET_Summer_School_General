#!/usr/local/bin/python3
# Plot Amdahl's Law

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize=(5, 5))
S = [0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
nPoints = 14
legend = []
for j, s in enumerate(S):
    P = 1-s
    SpeedUp = np.ndarray(shape=(2, nPoints))

    for i in range(nPoints):
        N = pow(2, i*0.5)
        SpeedUp[0, i] = N
        SpeedUp[1, i] = N-s*(N-1)

    plt.plot(SpeedUp[0, :], SpeedUp[1, :])
    legend.append("s = " '{:.2f}'.format(s))
#plt.title("Gustafson's Law")
plt.legend(legend)
plt.ylabel("Speed up")
plt.xlabel("Number of CPUs")
plt.grid(True)
plt.ylim((1, N))
plt.xlim((1, N))
plt.show()


plt.figure(figsize=(5, 5))
S = [0.1, 0.2, 0.4, 0.6, 0.8, 0.9]
nPoints = 14
legend = []
for j, s in enumerate(S):
    P = 1-s
    SpeedUp = np.ndarray(shape=(2, nPoints))
    Efficiency = np.ndarray(shape=(2, nPoints))
    for i in range(nPoints):
        N = pow(2, i*0.5)
        SpeedUp[0, i] = N
        SpeedUp[1, i] = N-s*(N-1)
        Efficiency[1, i] = SpeedUp[1, i]*100/N

    plt.plot(SpeedUp[0, :], Efficiency[1, :])
    legend.append("s = " '{:.2f}'.format(s))
# plt.title("Gustafson's Law")
plt.legend(legend, loc="upper right")
plt.ylabel("Efficiency, %")
plt.xlabel("Number of CPUs")
plt.grid(True)
plt.ylim((0, 100))
plt.xlim((1, N))
plt.show()
