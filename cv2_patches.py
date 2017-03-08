#!/usr/bin/env python
"""

"""

from __future__ import print_function

from cv2 import *


class VideoReader(object):
    "Wrapper for cv2.VideoCapture which makes it more pythonic."
    def __init__(self, source):
        self._video = VideoCapture(source)
    def __iter__(self):
        return self
    def __next__(self):
        self._video.grab()
        # TODO: test how expensive retrieve() is; if it's expensive, add a skip() method which *just* calls .grab()
        continue_, frame = self._video.retrieve()
        if continue_:
            # FIXME: maybe this should return (self.frame, self.msec, frame)?
            return frame
        else:
            raise StopIteration

    def __len__(self):
        return self._count

    def vidproperty(prop, type=None, doc=""):
        # "or None" translates 0s to Nones because "Note: When querying a property that is not supported by the backend used by the VideoCapture class, value 0 is returned."    
        def get(self):
            val = self._video.get(prop)
            if type is not None:
                # coerce to type
                val = type(val)
            return val
        def set(self, val):
            if not self._video.set(prop, val):
                raise ValueError(val) # TODO: include the (readable) name of the property
        return property(get, set, doc=doc)

    # properties of the video
    # http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
    # TODO
    width = vidproperty(CAP_PROP_FRAME_WIDTH, int, "Width of the frames in the video stream")
    height = vidproperty(CAP_PROP_FRAME_HEIGHT, int, "Height of the frames in the video stream")
    fps = vidproperty(CAP_PROP_FPS, float, "Frame rate")
    codec = vidproperty(CAP_PROP_FOURCC, doc="4-character code of codec")
    format = vidproperty(CAP_PROP_FORMAT, doc="Format of the Mat objects returned by next()")
    _msec = vidproperty(CAP_PROP_POS_MSEC, float, "Current position of the video file in milliseconds or video capture timestamp")
    _count = vidproperty(CAP_PROP_FRAME_COUNT, int, "Number of frames in the video file.")
    # FIXME: this one is tricky; the C++ API defines it as the index of the *next* frame to get .retrieve()d
    # does that mean the next call to next()?? 
    _frame = vidproperty(CAP_PROP_POS_FRAMES, int, doc="1-based index of the current frame")
    # maybe we should just censor this one
    # 

    # to compute the msec
    # i/fps (e.g. at 30fps, the 30th frame


if __name__ == '__main__':
    # simple barebones test
    # cv2_patches.py vid.mp4 -> see the frames printed 
    import sys
    vid = VideoReader(sys.argv[1])
    print("%d %dx%d frames @ %ffps" % (len(vid), vid.width, vid.height, vid.fps))
    print("codec: %s, format: %s" % (vid.codec, vid.format))
    for i, frame in enumerate(vid):
        print("Frame %d (compare: %d)" % (i, vid._frame))
        print("%0.2f ms should = %f s" % (vid._msec, i/vid.fps))
        print(frame.shape)
        #print(frame) 
        #input("Press enter to continue")
        print()
