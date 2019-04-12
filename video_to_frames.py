'''
Within this script, focus to get the frames of the input video file.

Requirements
----
You require OpenCV 3.2 to be installed.

Run
----
If need to run this script seperately, then can edit the releavant input file path and output file path.

If need to use this script within another code then can import the scirpt and call the functions with relevant arguments.
'''

import cv2
import os

def get_frames(video_input_path, frame_output_path):

    if (os.path.isfile(video_input_path)):

        # Playing the input video from file
        video_capture = cv2.VideoCapture(video_input_path)

        try:
            if not os.path.exists(frame_output_path):
                os.makedirs(frame_output_path)
        except OSError:
            print('Error: Creating directory of data')

        # Capture the very first frame
        return_status, frame = video_capture.read()

        current_frame = 0
        while(return_status):
            # Saving the current frame's image as a jpg file
            frame_location = frame_output_path+"frame" + str(current_frame) + ".jpg"
            print ("Creating..." + frame_location)
            cv2.imwrite(frame_location, frame)
            # Increasing the current frame value for the next frame
            current_frame += 1
            # Capture frame-by-frame
            return_status, frame = video_capture.read()

        # Release the capture
        video_capture.release()
        cv2.destroyAllWindows()
    else:
        print("Invalid input video to capture. Location or the video not exist.")

def run():
    path = 'D:\Campus\FYP\SumMe\\videos\\notre_dame.mp4'
    #video_input_path = os.path.join("D:","Campus","FYP","SumMe",)
    video_input_path = path
    frame_output_path = "generated_frames/"
    get_frames(video_input_path, frame_output_path)

if __name__ == "__main__":
    run()