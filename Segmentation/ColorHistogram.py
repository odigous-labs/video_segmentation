import os

import cv2
import numpy as np

from Segmentation import HistQueue, get_histograms, CombinedHist


class ColorHistogram:
    # this is to save the file numbers
    x = []
    # following arrays will store red,green and blue histogram values of each file
    y_red = []
    y_green = []
    y_blue = []

    list_of_files = []
    queue_of_hists = HistQueue.HistQueue(0)
    path_to_frames_directory = ""
    sampling_rate = 0

    def __init__(self, path_to_frames_directory, sampling_rate=25):
        # TODO Handle the exception for file not found error
        self.list_of_files = os.listdir(path_to_frames_directory)
        self.queue_of_hists = HistQueue.HistQueue(sampling_rate)
        self.path_to_frames_directory = path_to_frames_directory
        self.sampling_rate = sampling_rate
        # this is to save the file numbers
        self.x = []
        # following arrays will store red,green and blue histogram values of each file
        self.y_red = []
        self.y_green = []
        self.y_blue = []

    def compare(self, current_hist, frame_no):

        avg_histr = self.queue_of_hists.getAverageHist()
        red_result = cv2.compareHist(current_hist.getRedHistr(), avg_histr.getRedHistr(), 0)
        green_result = cv2.compareHist(current_hist.getGreenHistr(), avg_histr.getGreenHistr(), 0)
        blue_result = cv2.compareHist(current_hist.getBlueHistr(), avg_histr.getBlueHistr(), 0)

        self.x.append(frame_no)
        self.y_red.append(red_result)
        self.y_green.append(green_result)
        self.y_blue.append(blue_result)

    def get_shots_forward(self):
        number_of_files = len(self.list_of_files)
        for i in range(0, number_of_files):
            blue_histr, green_histr, red_histr = get_histograms.get_histograms(
                self.path_to_frames_directory + '/frame' + str(i) + ".jpg")
            hist_of_image = CombinedHist.CombinedHist(blue_histr, green_histr, red_histr)
            self.compare(hist_of_image, i)
            self.queue_of_hists.insert_histr(hist_of_image)
        y = np.add(np.add(self.y_red, self.y_green), self.y_blue) / 3
        return y

    def get_shots_backward(self):
        number_of_files = len(self.list_of_files)
        for i in range(number_of_files - 1, -1, -1):
            blue_histr, green_histr, red_histr = get_histograms.get_histograms(
                self.path_to_frames_directory + '/frame' + str(i) + ".jpg")
            hist_of_image = CombinedHist.CombinedHist(blue_histr, green_histr, red_histr)
            self.compare(hist_of_image, i)
            self.queue_of_hists.insert_histr(hist_of_image)
            print(i)
        y = np.add(np.add(self.y_red, self.y_green), self.y_blue) / 3
        return y
