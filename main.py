import create_shot_boundaries
import video_to_frames
from frame_seperater import FrameSeperator


def run():
    video_to_frames.run()
    shot_boundaries = create_shot_boundaries.run('generated_frames')
    print("Folder Creating Process Started")
    frame_seperator = FrameSeperator(shot_boundaries)
    frame_seperator.create_folders()
    print("Process Finished Successfully")

if __name__ == "__main__":
    run()