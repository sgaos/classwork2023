import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0,10,0.1)
y = np.sin(t)

plt.plot(t,y)
plt.show()