import cv2
import os
from Segmentation import get_histograms

listofFiles = os.listdir('generated_frames')

reference_histr_blue,reference_histr_green,reference_histr_red = get_histograms.\
    get_histograms('generated_frames/frame0.jpg')

for i,file in enumerate(listofFiles):
    histr_blue,histr_green,histr_red = get_histograms.get_histograms('generated_frames/' + file)
    red = cv2.compareHist(reference_histr_red,histr_red,0)
    print(i)
    print(red)