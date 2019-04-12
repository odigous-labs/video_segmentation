import cv2


#this function will return 3 arrays as histograms of a given image
def get_histograms(file_path):

    #String file_name - path for the image file we need to get the oolor histogram
    img = cv2.imread(file_path)
    blue_histr = cv2.calcHist([img],[0],None,[256],[0,256])
    green_histr = cv2.calcHist([img], [1], None, [256], [0, 256])
    red_histr = cv2.calcHist([img], [2], None, [256], [0, 256])
    return blue_histr,green_histr,red_histr