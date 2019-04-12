import numpy as np

#Thia class can be used as the data structure to store all the histograms in a single #image

class CombinedHist:

    # arrrays to store red,green,blue histogram components
    blue_hist= np.zeros((256,1))
    green_hist= np.zeros((256,1))
    red__hist = np.zeros((256,1))

    def __init__(self, blue_hist, green_hist, red_hist):
        self.blue_hist = blue_hist
        self.green_hist = green_hist
        self.red__hist = red_hist

    # return red_histr
    def getRedHistr(self):
        return self.red__hist

    # return blue histr
    def getBlueHistr(self):
        return self.blue_hist

    # return green histr
    def getGreenHistr(self):
        return self.green_hist
