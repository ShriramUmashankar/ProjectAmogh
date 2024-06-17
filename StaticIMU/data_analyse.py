
import matplotlib.pyplot as plt
import numpy as np

inside = np.loadtxt('/home/shriram/Documents/Amogh/data/inside.txt',dtype=str)
outside = np.loadtxt('/home/shriram/Documents/Amogh/data/outside.txt',dtype=str)

yaw_inside=[]
yaw_outside=[]

for i in range(inside.shape[0]):
    val=inside[i].split(',')
    yaw_inside.append(float(val[2])*180/np.pi)

for i in range(outside.shape[0]):
    val=outside[i].split(',')
    yaw_outside.append(float(val[2])*180/np.pi)

plt.figure(figsize=(12,10))

plt.plot(yaw_inside,'-b')
plt.plot(yaw_outside,'-r')
plt.grid()

plt.show()
