from queue import *
from Segmentation import CombinedHist
import numpy as np


#Thia class is a queuse of histograms
class HistQueue:
    size = 0
    added_elements = 0
    hist_queue = Queue()

    total_blue_histr = np.zeros((256,1),dtype = np.float32)
    total_green_histr = np.zeros((256,1),dtype = np.float32)
    total_red_histr = np.zeros((256,1),dtype = np.float32)

    # initializer
    def __init__(self, size):
        self.size = size
        self.hist_queue = Queue(size)

    # this will insert a new histr to qwuee
    # if the queue is full this will remove the first element and
    # then insert the new histr
    def insert_histr(self, combined_histr):
        self.added_elements +=1
        if self.hist_queue.qsize() < self.size:
            self.hist_queue.put(combined_histr)
            self.increaseTotalValues(combined_histr)
        else:
            removed_hist = self.hist_queue.get()
            self.decreaseTotalValues(removed_hist)
            self.hist_queue.put(combined_histr)
            self.increaseTotalValues(combined_histr)

    # this will return the size of the queue
    def getMaximumSize(self):
        return self.size

    # this will return the number of elements currently added to the queue
    def getAddedNoOfHistr(self):
        return self.added_elements

    #this will return an average hist from the elements in the queue
    def getAverageHist(self):
        if self.added_elements>0:
            avg_blue_histr = self.total_blue_histr/self.added_elements
            avg_green_histr = self.total_green_histr / self.added_elements
            avg_red_histr = self.total_red_histr / self.added_elements
            return CombinedHist.CombinedHist(avg_blue_histr, avg_green_histr, avg_red_histr)
        else:
            return CombinedHist.CombinedHist(np.zeros((256, 1), dtype = np.float32), np.zeros((256, 1), dtype = np.float32), np.zeros((256, 1), dtype = np.float32))

    #this will increase the total values for a given hist
    def increaseTotalValues(self,cmbHist):
        #cmbHist = CombinedHist.CombinedHist(CombinedHists)
        self.total_blue_histr += cmbHist.getBlueHistr()
        self.total_green_histr += cmbHist.getGreenHistr()
        self.total_red_histr += cmbHist.getRedHistr()

    # this will increase the total values for a given hist
    def decreaseTotalValues(self, cmbHist):
        #cmbHist = CombinedHist.CombinedHist(CombinedHists)
        self.total_blue_histr -= cmbHist.getBlueHistr()
        self.total_green_histr -= cmbHist.getGreenHistr()
        self.total_red_histr -= cmbHist.getRedHistr()