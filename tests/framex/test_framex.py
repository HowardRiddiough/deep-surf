from deepsurf.framex import SurfFrames


def test_init():
    interval = 60
    out_path = "./"
    sf = SurfFrames(interval, out_path)
    assert sf.interval == 60
    assert sf.out_path == out_path
