import cv2
import numpy as np
from matplotlib import pyplot as plt

file0 = 'image.jpg'
img = cv2.imread(file0)
color = ('b','g','r')
plt.figure()
allHist = (256,256)
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    allHist += histr
    plt.plot(histr,color = col)
    plt.xlim([0,256])
allHist = allHist/3
plt.plot(allHist,'k')
plt.show()