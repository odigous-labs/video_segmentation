from Segmentation import Segment


segment = Segment.Segment(path_to_frames_directory='generated_frames',sampling_rate=25)
segment.get_shots()