import os
import cv2
from Segmentation import CombinedHist, get_histograms, HistQueue
import matplotlib.pyplot as plt
import numpy as np

listofFiles = os.listdir('generated_frames')
#change the size of queue accordingly
queue_of_hists = HistQueue.HistQueue(25)
x =[]
y_r=[]
y_g = []
y_b = []

def compare(current_hist,frame_no):
    avg_histr = queue_of_hists.getAverageHist()
    red_result = cv2.compareHist(current_hist.getRedHistr(),avg_histr.getRedHistr(),0)
    green_result = cv2.compareHist(current_hist.getGreenHistr(), avg_histr.getGreenHistr(), 0)
    blue_result = cv2.compareHist(current_hist.getBlueHistr(), avg_histr.getBlueHistr(), 0)

    x.append(i)
    y_r.append(red_result)
    y_g.append(green_result)
    y_b.append(blue_result)

    #print(red_result)



for i in range (0,4000):
    blue_histr, green_histr, red_histr = get_histograms.get_histograms('generated_frames/frame' + str(i) + ".jpg")
    hist_of_image = CombinedHist.CombinedHist(blue_histr, green_histr, red_histr)
    compare(hist_of_image,i)
    queue_of_hists.insert_histr(hist_of_image)
    print ("frame"+str(i)+".jpg")

fig = plt.figure(figsize=(18, 5))



y = np.add(np.add(y_r,y_g),y_b)/3
value =np.percentile(y,5)

median  =  np.median(y)
minimum = np.amin(y)
y_sorted = np.sort(y)
getting_index = y_sorted[8]
print ("quartile"+str(value))
print ("median"+str(median))
plt.plot(x,y,color = 'k')
plt.axhline(y=value, color='r', linestyle='-')
plt.xticks(np.arange(min(x), max(x)+1, 100.0))
plt.show()