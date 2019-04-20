from Segmentation import Segment
import numpy as np
from matplotlib import pyplot as plt
import scipy.cluster.hierarchy as hcluster


segment1 = Segment.Segment(path_to_frames_directory='D:\Campus\FYP\Video_segmentation\generated_frames',sampling_rate=25)
forward_dict = segment1.get_shots_forward()
segment2 = Segment.Segment(path_to_frames_directory='D:\Campus\FYP\Video_segmentation\generated_frames',sampling_rate=25)
backward_dict = segment2.get_shots_backward()
# forward_x = []
# forward_y = []
# backward_x=[]
# backward_y = []
data = []
for frame in forward_dict:
    x=frame.get_frame_no()
    y=frame.get_correlation_val()
    coordinate = [x,y]
    data.append(coordinate)
for frame in forward_dict:
    x=frame.get_frame_no()
    y=frame.get_correlation_val()
    coordinate = [x,y]
    data.append(coordinate)

data_array = np.array(data)
# for frame in backward_dict:
#     backward_x.append(frame.get_frame_no())
#     backward_y.append(frame.get_correlation_val())
# plt.scatter(forward_x,forward_y,color='b')
# plt.scatter(backward_x,backward_y,color='r')

# plt.show()
thresh = 5
clusters = hcluster.fclusterdata(data_array, thresh, criterion="distance")

# plotting
plt.scatter(*np.transpose(data_array), c=clusters)
plt.axis("equal")
title = "threshold: %f, number of clusters: %d" % (thresh, len(set(clusters)))
plt.title(title)
plt.show()
print("Process Finished Successfully")