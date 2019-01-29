from time import sleep
from datetime import datetime, timedelta, timezone
from urllib import request

from skyfield import api
from skyfield import almanac


SCHEVENINGEN_LATITUDE_DEGS = 52.10550355970487
SCHEVENINGEN_LONGITUDE_DEGS = 4.265012741088867

SURF_CAMS = {
        "surf_cam": "http://www.scheveningenlive.nl/cam_1.jpg"
    }

def is_dt_in_sunlight(
    dt_utc: datetime, 
    latitude: float = SCHEVENINGEN_LATITUDE_DEGS, 
    longitude: float = SCHEVENINGEN_LONGITUDE_DEGS
) -> bool:
    ts = api.load.timescale()
    e = api.load("de421.bsp")

    year, month, day = dt_utc.year, dt_utc.month, dt_utc.day

    t0 = ts.utc(year, month, day, 0)
    t1 = ts.utc(year, month, day, 24)

    location = api.Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    sunrise_sunset, y = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(e, location))
    sunrise, sunset = sunrise_sunset.utc_datetime()

    return sunrise <= dt_utc <= sunset