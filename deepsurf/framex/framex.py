from collections import OrderedDict
import os
import urllib
from datetime import datetime, timedelta, timezone
from time import sleep
import logging

import numpy as np
import cv2
from pytesseract import image_to_string
from skyfield import api
from skyfield import almanac

# logger = logging.getLogger(__file__)
# logger.setLevel(logging.INFO)

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


class SurfFrames:
    def __init__(self, interval: int, out_path: str):
        self.interval = interval
        self.out_path = out_path

    def get_frames(self):
#         logging.info("Downloading frames for {} cameras every {} seconds".format(len(CAMS), self.interval))
        while True:
            if SurfFrames.is_dt_in_sunlight(datetime.now(timezone.utc)):
                for cam_name, cam_url in CAMS.items():
                    self._persist_frame_to_disk(cam_url, self.out_path, cam_name)
                sleep(self.interval)
            else:
                sleep(self.interval)

    @staticmethod
    def _persist_frame_to_disk(url: str, out_path: str, cam_name: str):
        frame_array = SurfFrames._request_frame_as_array(url)
        cam_id, dt = SurfFrames._cam_id_timestamp_from_frame_text(frame_array, cam_name)
        cv2.imwrite(os.path.join(out_path, "{}_{}.jpg".format(cam_id, dt)), frame_array)

    @staticmethod
    def _request_frame_as_array(url: str):
        resp = urllib.request.urlopen(url)
        frame = np.asarray(bytearray(resp.read()), dtype="uint8")
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)

    @staticmethod
    def _cam_id_timestamp_from_frame_text(frame: np.ndarray, cam_name: str):
        x_min, x_max, y_min, y_max = CAM_CROP[cam_name].values()
        crop_frame = frame[y_min: y_max, x_min: x_max]
        cam_id, _, dt = image_to_string(crop_frame, lang="eng").lower().split("|")
        dt = datetime.strptime(dt, " %d-%m-%Y %H:%M:%S").strftime("%Y%m%d%H%M%S")
        return cam_id.replace(" ", ""), dt

    @staticmethod
    def is_dt_in_sunlight(
            dt_utc: datetime, latitude: float = SCH_LATITUDE_DEGS, longitude: float = SCH_LONGITUDE_DEGS
    ) -> bool:
        ts = api.load.timescale()
        e = api.load("de421.bsp")

        year, month, day = dt_utc.year, dt_utc.month, dt_utc.day

        t0 = ts.utc(year, month, day, 0)
        t1 = ts.utc(year, month, day, 24)

        location = api.Topos(latitude_degrees=latitude, longitude_degrees=longitude)

        sunrise_sunset, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(e, location))
        sunrise, sunset = sunrise_sunset.utc_datetime()

        return sunrise - timedelta(minutes=20) <= dt_utc <= sunset + timedelta(minutes=20)
