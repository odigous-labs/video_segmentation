from Segmentation import Segment
import numpy as np
from matplotlib import pyplot as plt
import scipy.cluster.hierarchy as hcluster



def run(path_to_frames_directory):
    segment1 = Segment.Segment(path_to_frames_directory=path_to_frames_directory,
                               sampling_rate=25)
    forward_dict = segment1.get_shots_forward()
    segment2 = Segment.Segment(path_to_frames_directory=path_to_frames_directory,
                               sampling_rate=25)
    backward_dict = segment2.get_shots_backward()

    data = []
    for frame in forward_dict:
        x = frame.get_frame_no()
        y = frame.get_correlation_val()
        coordinate = [x, y]
        data.append(coordinate)
    for frame in forward_dict:
        x = frame.get_frame_no()
        y = frame.get_correlation_val()
        coordinate = [x, y]
        data.append(coordinate)

    data_array = np.array(data)
    x = data_array[:, :1]
    y = data_array[:, 1:2]

    thresh = 25
    clusters = hcluster.fclusterdata(data_array, thresh, criterion="distance")
    plt.scatter(*np.transpose(data_array), c=clusters)
    plt.show()
    cluster_dict = {}
    for i in range(clusters.max()):
        cluster_dict[str(i + 1)] = []

    for i, val in enumerate(clusters):
        print(str(val))
        temp_list = cluster_dict[str(val)]
        temp_list.append(i)
        cluster_dict[str(val)] = temp_list

    shot_boundaries = []

    for key in cluster_dict.keys():
        minimum_frame_index = data_array[cluster_dict[key][0]][0]
        minimum_cor_value = data_array[cluster_dict[key][0]][1]
        for val in cluster_dict[key]:
            if (minimum_cor_value > data_array[val][1]):
                minimum_frame_index = data_array[val][0]
        shot_boundaries.append(minimum_frame_index)

    shot_boundaries.sort()
    return shot_boundaries

if __name__ == "__main__":
    run()