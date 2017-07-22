from model import SingleRoomModel
import matplotlib.pyplot as plt
import numpy as np

SingleRoom = SingleRoomModel(0,1)
x1, x2, z, y, y1 = SingleRoom.run_model()


print (y1)

plt.subplot(2, 2, 1)
plt.plot(range(z), x1, 'b')
#plt.title('Gas Partial Pressures')
plt.grid(True)
plt.ylabel('Oxygen (kPa)')
plt.xlabel('Time (hours)')

plt.subplot(2, 2, 2)
plt.plot(range(z), x2, 'r')
plt.xlabel('Time (hours)')
plt.ylabel('Carbon Dioxide (kPa)')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(range(z), y, 'g')
plt.xlabel('Time (hours)')
plt.ylabel('People')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(range(z), y1, 'y')
plt.xlabel('Time (hours)')
plt.ylabel('Plants')
plt.grid(True)

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.suptitle("Gas Partial Pressures",fontsize=14)
plt.show()
