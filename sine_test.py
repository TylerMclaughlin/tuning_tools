import numpy as np
import matplotlib.pyplot as plt


theta = np.linspace(0,20,800)

# exists
#plt.plot(np.sin(1*theta))
# exists
#plt.plot(np.sin(7*theta))
# exists?
plt.plot(np.sin(2*theta))
#plt.plot(np.sin(3*theta))
#plt.plot(np.sin(4*theta))
plt.plot(np.sin(3*theta) + np.sin(4*theta))
plt.show()
