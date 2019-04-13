class Frame:

    frame_no=None
    #this is the correlation value with the averaged histogram
    correlation_val =None

    def __init__(self,frame_no=None,correlation_val=None):
        self.frame_no = frame_no
        self.correlation_val = correlation_val

    def get_frame_no(self):
        return self.frame_no

    def get_correlation_val(self):
        return  self.correlation_val
