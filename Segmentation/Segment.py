from Segmentation import HistQueue, get_histograms, CombinedHist, Frame
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


class Segment:
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
            print(i)
        fig = plt.figure(figsize=(18, 5))
        y = np.add(np.add(self.y_red, self.y_green), self.y_blue) / 3
        frames_less_than_threshold = self.seperate_frames_forward(summed_hist=y, threshold=7)

        shot_boundaries_dict =self.detect_boundaries_forward(frames_less_than_threshold,self.sampling_rate)
        shot_frames =self.detect_frame(shot_boundaries_dict)
        smoothed_shot_boundaries = self.smooth_boundaries_forward(shot_frames)
        value = np.percentile(y, 10)
        median = np.median(y)
        minimum = np.amin(y)
        y_sorted = np.sort(y)
        getting_index = y_sorted[8]
        print("quartile" + str(value))
        print("median" + str(median))
        plt.plot(self.x, y, color='k')
        plt.axhline(y=value, color='r', linestyle='-')
        plt.xticks(np.arange(min(self.x), max(self.x) + 1, 100.0))
        plt.show()
        #return smoothed_shot_boundaries
        return frames_less_than_threshold

    def get_shots_backward(self):
        number_of_files = len(self.list_of_files)
        for i in range(number_of_files-1,0,-1):
            blue_histr, green_histr, red_histr = get_histograms.get_histograms(
                self.path_to_frames_directory + '/frame' + str(i) + ".jpg")
            hist_of_image = CombinedHist.CombinedHist(blue_histr, green_histr, red_histr)
            self.compare(hist_of_image, i)
            self.queue_of_hists.insert_histr(hist_of_image)
            print(i)
        fig = plt.figure(figsize=(18, 5))
        y = np.add(np.add(self.y_red, self.y_green), self.y_blue) / 3
        frames_less_than_threshold = self.seperate_frames_backward(summed_hist=y, threshold=5)

        #shot_boundaries_dict =self.detect_boundaries_backward(frames_less_than_threshold,self.sampling_rate)
        #shot_frames =self.detect_frame(shot_boundaries_dict)
        #smoothed_shot_boundaries = self.smooth_boundaries_backward(shot_frames)
        #return smoothed_shot_boundaries
        return  frames_less_than_threshold

    # this method wil seperate the frames less than the threshold and return a list with each frame with the correlation
    # value
    def seperate_frames_forward(self, summed_hist, threshold):
        threshold_value = np.percentile(summed_hist, threshold)
        frames_less_than_threshold = []
        for i, val in enumerate(summed_hist):
            if (val < threshold_value):
                frame = Frame.Frame(i, val)
                frames_less_than_threshold.append(frame)
        return frames_less_than_threshold

    # this method wil seperate the frames less than the threshold and return a list with each frame with the correlation
    # value
    def seperate_frames_backward(self, summed_hist, threshold):
        threshold_value = np.percentile(summed_hist, threshold)
        frames_less_than_threshold = []
        size = len(summed_hist)
        for i, val in enumerate(summed_hist):
            if (val < threshold_value):
                frame = Frame.Frame(size-i, val)
                frames_less_than_threshold.append(frame)
        return frames_less_than_threshold


    # thia will seperate shot boundaries considering the sampling rate
    # This will cateogarize the detectetd frames by sampling rate
    def detect_boundaries_forward(self, frames_less_than_threshold, sampling_rate):

        # this will store the base frame to detect whether a frame is too far away from a currently detected shot
        # boundary
        base_frame = frames_less_than_threshold[0].get_frame_no()
        # this will keep track of the number of shots
        shot_number = 1
        # this list will store the frames belong to a certain shot boundary
        shot = []
        shot_boundaries_dict = {}
        for i in frames_less_than_threshold:
            current_frame_number = i.get_frame_no()
            value = i.get_correlation_val()
            if ((current_frame_number - base_frame) < sampling_rate):
                shot.append(i)
            else:
                shot_boundaries_dict["shot_"+str(shot_number)] = shot
                shot_number +=1
                shot = [i]
                base_frame = current_frame_number
        shot_boundaries_dict["shot_" + str(shot_number)] = shot
        return shot_boundaries_dict

    #
    def detect_frame(self,shot_boundaries_dict):
        dict_of_shots = {}
        for key in shot_boundaries_dict:
            min = shot_boundaries_dict[key][0]
            for i in shot_boundaries_dict[key]:
                if i.get_correlation_val() < min.get_correlation_val() :
                    min = i
            dict_of_shots[key] = min
        return dict_of_shots

    def smooth_boundaries_forward(self,shot_frames):
        frames_list = []
        current_frame = shot_frames[next(iter(shot_frames))]
        temp_list_to_neighboring_frames = [current_frame]
        for key in shot_frames:
            frame_to_compare = shot_frames[key]
            if (frame_to_compare.get_frame_no() - current_frame.get_frame_no()) < self.sampling_rate:
                temp_list_to_neighboring_frames.append(frame_to_compare)
            else:
                minimum_frame = self.get_grame_with_minimum_correlation_value(temp_list_to_neighboring_frames)
                frames_list.append(minimum_frame)
                temp_list_to_neighboring_frames = [frame_to_compare]
                current_frame = frame_to_compare
        minimum_frame = self.get_grame_with_minimum_correlation_value(temp_list_to_neighboring_frames)
        frames_list.append(minimum_frame)
        return frames_list

    # retufn the frame with the minimum correlation value in a given list of frames
    def get_grame_with_minimum_correlation_value(self,list_of_frames):
        minimum_frame =list_of_frames[0]
        for frame in list_of_frames:
            if minimum_frame.get_correlation_val()> frame.get_correlation_val():
                minimum_frame = frame

        return minimum_frame

    def detect_boundaries_backward(self, frames_less_than_threshold, sampling_rate):

        # this will store the base frame to detect whether a frame is too far away from a currently detected shot
        # boundary
        base_frame = frames_less_than_threshold[0].get_frame_no()
        # this will keep track of the number of shots
        shot_number = 1
        # this list will store the frames belong to a certain shot boundary
        shot = []
        shot_boundaries_dict = {}
        for i in frames_less_than_threshold:
            current_frame_number = i.get_frame_no()
            value = i.get_correlation_val()
            if (( base_frame-current_frame_number) < sampling_rate):
                shot.append(i)
            else:
                shot_boundaries_dict["shot_"+str(shot_number)] = shot
                shot_number +=1
                shot = [i]
                base_frame = current_frame_number
        shot_boundaries_dict["shot_" + str(shot_number)] = shot
        return shot_boundaries_dict

    def smooth_boundaries_backward(self,shot_frames):
        frames_list = []
        current_frame = shot_frames[next(iter(shot_frames))]
        temp_list_to_neighboring_frames = [current_frame]
        for key in shot_frames:
            frame_to_compare = shot_frames[key]
            if (current_frame.get_frame_no() - frame_to_compare.get_frame_no()  ) < self.sampling_rate:
                temp_list_to_neighboring_frames.append(frame_to_compare)
            else:
                minimum_frame = self.get_grame_with_minimum_correlation_value(temp_list_to_neighboring_frames)
                frames_list.append(minimum_frame)
                temp_list_to_neighboring_frames = [frame_to_compare]
                current_frame = frame_to_compare
        minimum_frame = self.get_grame_with_minimum_correlation_value(temp_list_to_neighboring_frames)
        frames_list.append(minimum_frame)
        return frames_list