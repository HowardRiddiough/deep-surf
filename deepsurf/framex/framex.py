from collections import OrderedDict
import os
import urllib.request
from datetime import datetime
from time import sleep
import logging

import numpy as np
import cv2
from pytesseract import image_to_string

logger = logging.getLogger(__file__)
logger.setLevel(logging.WARN)

CAMS = dict(
    surf="http://www.scheveningenlive.nl/cam_1.jpg",
    sports="http://www.scheveningenlive.nl/sport.jpg"
)

CAM_CROP = dict(
    sports=OrderedDict(
        x_min=30,
        x_max=550,
        y_min=0,
        y_max=20
    ),
    surf=OrderedDict(
        x_min=40,
        x_max=850,
        y_min=0,
        y_max=25
    )
)

SCH_LATITUDE_DEGS = 52.10550355970487
SCH_LONGITUDE_DEGS = 4.265012741088867
EXPECTED_IMAGE_TEXT_TUPLE_LENGTH = 3


class SurfFramesException(Exception):
    pass


class SurfFrames:
    def __init__(self, interval: int, out_path: str, logging_level: str = "silent"):
        """Provides functionality to download image date from 2 web cams hosted on scheveningenlive.nl and
        is thus a handy tool to collect data for deep learning. Images downloaded will be saved to `out_path`.
         The file naming is dynamic: timestamp is concatenated to the camera id.

        Args:
            interval: Proved in seconds, images will be downloaded every `interval` seconds
            out_path: The path where images will be saved
            logging_level: Set the logging level. Default is silent, other options: loud
        """
        self.interval = interval
        self.out_path = out_path

        if logging_level == "loud":
            logger.setLevel(logging.INFO)

    def get_frames(self):
        """Constantly saves frames to `self.out_path` with a sleep time between downloads of `self.interval`.
        """
        logger.info("Downloading frames for {} cameras every {} seconds".format(len(CAMS), self.interval))
        while True:
            for cam_name, cam_url in CAMS.items():
                self._persist_frame_to_disk(cam_url, self.out_path, cam_name)

            logger.info("Sleeping for {} seconds".format(self.interval))
            sleep(self.interval)

    @staticmethod
    def _persist_frame_to_disk(url: str, out_path: str, cam_name: str):
        """Saves frame to disk with dynamic naming. Timestamps are inferred from the frame using OCR.

        Args:
            url: Url of web cam image
            out_path: Path where to save images
            cam_name: Name of camera
        """
        frame_array = SurfFrames._request_frame_as_array(url)
        try:
            cam_id, dt = SurfFrames._cam_id_timestamp_from_frame_text(frame_array, cam_name)
            cv2.imwrite(os.path.join(out_path, "{}_{}.jpg".format(cam_id, dt)), frame_array)
            logger.info("Saved {} frame to: {}".format(cam_id, out_path))
        except SurfFramesException:
            logger.info("Could not extract text from {} frame".format(cam_name))
            pass

    @staticmethod
    def _request_frame_as_array(url: str) -> np.ndarray:
        """Uses urllib to return the webc am image as an numpy array

        Args:
            url: Url of web cam image
        """
        resp = urllib.request.urlopen(url)
        frame = np.asarray(bytearray(resp.read()), dtype="uint8")
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)

    @staticmethod
    def _cam_id_timestamp_from_frame_text(frame: np.ndarray, cam_name: str):
        """Uses OCR to infer the timestamp from an image.

        Args:
            frame: A frame provided as np.ndarray
            cam_name: Name of camera

        Returns:
            tuple of unique cam id and timestamp
        """
        x_min, x_max, y_min, y_max = CAM_CROP[cam_name].values()
        crop_frame = frame[y_min: y_max, x_min: x_max]
        image_text = image_to_string(crop_frame, lang="eng").lower().split("|")

        if len(image_text) != EXPECTED_IMAGE_TEXT_TUPLE_LENGTH:
            raise SurfFramesException(
                "Text does not match expected format. Text extracted:\n{}".format(image_text)
            )
        else:
            cam_id, _, dt = image_text

        dt = datetime.strptime(dt, " %d-%m-%Y %H:%M:%S").strftime("%Y%m%d%H%M%S")
        return cam_id.replace(" ", ""), dt
