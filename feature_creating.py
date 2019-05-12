from Segmentation import ColorHistogram
from Segmentation import MatrixDistance


def run():
    forward = ColorHistogram.ColorHistogram('./generated_frames')
    backward = ColorHistogram.ColorHistogram('./generated_frames')
    mat_dis = MatrixDistance.MatrixDistance("./generated_frames")
    histogram_forward = forward.get_shots_forward()
    histogram_backward = backward.get_shots_backward()
    channel_0, channel_1, channel_2 = mat_dis.getMatDistanceValues()

    print("Values Calculated")


run()
