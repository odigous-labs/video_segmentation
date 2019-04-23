from shutil import copyfile,rmtree
import os

class FrameSeperator:
    shot_boundaries =[]
    path_to_generated_shots="generated_shots"

    def __init__(self,shot_boundaries):
        self.shot_boundaries = shot_boundaries
        if (os.path.isdir(self.path_to_generated_shots)):
            rmtree(self.path_to_generated_shots)
            os.mkdir(self.path_to_generated_shots)
        else:
            os.mkdir(self.path_to_generated_shots)

    def create_folders(self):
        prev_val = 0
        for i,val in enumerate(self.shot_boundaries):
            shot_path = self.path_to_generated_shots+"/"+str(i+1)
            os.mkdir(shot_path)
            int_val = int(val)
            for num in range (prev_val,int(val)):
                src = "generated_frames/frame"+str(num)+".jpg"
                dst = shot_path+"/frame"+str(num)+".jpg"
                copyfile(src,dst)
            prev_val = int(val)