from utils.imgTransform import cartoon_effect, edge_detect, face_detect, face_detect_cvlib, gender_recog_cvlib, object_detect_cvlib, rotate_track
from utils.mobilenet import mobilenet
from aiortc import MediaStreamTrack
from av import VideoFrame


class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """
    start_frame_number = 50
    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform

    async def recv(self):
        frame = await self.track.recv()
        img = frame.to_ndarray(format="bgr24")
        
        if self.transform == "object":
            img = object_detect_cvlib(img)

        elif self.transform == "face":
            img = face_detect(img)

        elif self.transform == "facecv":
            img = face_detect_cvlib(img)

        elif self.transform == "gender":
            img = gender_recog_cvlib(img)

        elif self.transform == "edges":
            img = edge_detect(img)

        elif self.transform == "rotate":
            img = rotate_track(img, frame.time)

        elif self.transform == "cartoon":
            img = cartoon_effect(img)

        elif self.transform == 'mobilenet':
            img = mobilenet(img)

        else:
            # No transformation at all
            return frame

        # rebuild a VideoFrame, preserving timing information
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame
