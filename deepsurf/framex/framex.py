import os
import urllib
from datetime import datetime, timedelta, timezone
from time import sleep

import numpy as np
import cv2
from pytesseract import image_to_string
from skyfield import api
from skyfield import almanac

X = 0
Y = 0
H = 30
W = 1280

SCH_LATITUDE_DEGS = 52.10550355970487
SCH_LONGITUDE_DEGS = 4.265012741088867

SURF_CAM_URL = "http://www.scheveningenlive.nl/cam_1.jpg"


class SurfFrames:
    def __init__(self, interval: int, out_path: str, cam_url: str = SURF_CAM_URL):
        self.interval = interval
        self.out_path = out_path
        self.cam_url = cam_url

    def get_frames(self):
        while True:
            if SurfFrames.is_dt_in_sunlight(datetime.now(timezone.utc)):
                self._persist_frame_to_disk(self.cam_url, self.out_path)
                sleep(self.interval)
            else:
                sleep(self.interval)

    @staticmethod
    def _persist_frame_to_disk(url: str, out_path: str):
        frame_array = SurfFrames._request_frame_as_array(url)
        cam_id, dt = SurfFrames._cam_id_timestamp_from_frame_text(frame_array)
        cv2.imwrite(os.path.join(out_path, "{}_{}.jpg".format(cam_id, dt)), frame_array)

    @staticmethod
    def _request_frame_as_array(url: str):
        resp = urllib.request.urlopen(url)
        frame = np.asarray(bytearray(resp.read()), dtype="uint8")
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)

    @staticmethod
    def _cam_id_timestamp_from_frame_text(frame: np.ndarray):
        crop_frame = frame[Y: Y + H, X: X + W]
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
