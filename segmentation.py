import os
import cv2
import CombinedHist
import get_histograms
import HistQueue

listofFiles = os.listdir('generated_frames')
#change the size of queue accordingly
queue_of_hists = HistQueue.HistQueue(10)

def compare(current_hist):
    avg_histr = queue_of_hists.getAverageHist()
    red_result = cv2.compareHist(current_hist.getRedHistr(),avg_histr.getRedHistr(),0)
    print(red_result)

for i, file in enumerate(listofFiles):
    blue_histr, green_histr, red_histr = get_histograms.get_histograms('generated_frames/'+file)
    hist_of_image = CombinedHist.CombinedHist( blue_histr, green_histr, red_histr)
    compare(hist_of_image)
    queue_of_hists.insert_histr(hist_of_image)
    print (file)

