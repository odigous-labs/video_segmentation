import os

import cv2
import numpy as np


class MatrixDistance:
    path_to_frames_directory = ""
    list_of_files = []
    distance_value_channel_0 = []
    distance_value_channel_1 = []
    distance_value_channel_2 = []

    def __init__(self, path_to_frames_directory):
        self.path_to_frames_directory = path_to_frames_directory
        self.list_of_files = os.listdir(path_to_frames_directory)

    def getMatDistanceValues(self):
        number_of_files = len(self.list_of_files)
        channel_0 = None
        channel_1 = None
        channel_2 = None
        for i in range(0, number_of_files):
            # We cannot compare the values of the first frame,when the first frame is in the loop we need to set the
            # values in the above variables and then set the distant value of the first frame to zero
            if (channel_2 is None) & (channel_1 is None) & (channel_0 is None):
                channel_0, channel_1, channel_2 = self.getImage(i)
                self.distance_value_channel_0.append(0)
                self.distance_value_channel_1.append(0)
                self.distance_value_channel_2.append(0)
            else:
                cur_channel_0, cur_channel_1, cur_channel_2 = self.getImage(i)
                compared_channel_0, compared_channel_1, compared_channel_2 = self.compareChannels(channel_0, channel_1,
                                                                                                  channel_2,
                                                                                                  cur_channel_0,
                                                                                                  cur_channel_1,
                                                                                                  cur_channel_2)
                channel_0_distance = self.getDistanceValue(compared_channel_0)
                channel_1_distance = self.getDistanceValue(compared_channel_1)
                channel_2_distance = self.getDistanceValue(compared_channel_2)
                self.distance_value_channel_0.append(channel_0_distance)
                self.distance_value_channel_1.append(channel_1_distance)
                self.distance_value_channel_2.append(channel_2_distance)
        return self.distance_value_channel_0, self.distance_value_channel_1, self.distance_value_channel_2

    # returns each channel as a matrix of a given frame
    def getImage(self, frame_number):
        image = cv2.imread(self.path_to_frames_directory + '/frame' + str(frame_number) + ".jpg")
        # resized_image  = cv2.resize(image,(5,5))
        chnl0, chnl1, chnl2 = cv2.split(image)
        chnl0 = chnl0.astype('int32')
        chnl1 = chnl1.astype('int32')
        chnl2 = chnl2.astype('int32')
        return chnl0, chnl1, chnl2

    def compareChannels(self, prev_channel_0, prev_channel_1, prev_channel_2, curr_channel_0, curr_channel_1,
                        curr_channel_2):
        compared_mat_channel_0 = curr_channel_0 - prev_channel_0
        compared_mat_channel_1 = curr_channel_1 - prev_channel_1
        compared_mat_channel_2 = curr_channel_2 - prev_channel_2
        return compared_mat_channel_0, compared_mat_channel_1, compared_mat_channel_2

    def getDistanceValue(self, matrix):
        absolute_matrix = np.absolute(matrix)
        return np.sum(absolute_matrix)
