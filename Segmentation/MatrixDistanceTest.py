import MatrixDistance
import matplotlib.pyplot as plt

matdis = MatrixDistance.MatrixDistance("../generated_frames")
channel_0, channel_1, channel_2 = matdis.getMatDistanceValues()

plt.plot(channel_0, c='r')
plt.plot(channel_1, c='g')
plt.plot(channel_2, c='b')
plt.show()
