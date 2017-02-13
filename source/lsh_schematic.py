from matplotlib import pyplot as plt
import numpy as np

"""
Just a function for demonstrating the lsh collision probabilities.
"""
f, a = plt.subplots()
for m in [10]:
    for k in [10]:
        theta = np.linspace(0, 1, 100)
        a.plot(theta, 1 - (1 - theta ** k) ** m,
               label="m: " + str(m) + " , k " + str(k))

a.legend()
a.set_xlabel('Probability of collision')
a.set_ylabel('Prob. of being in one same bucket')

plt.show()

k = 10
