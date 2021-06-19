from ..main import Main
def test_video_returns_three_boards():
    instance = Main(recalibrate_camera = False, path = "test.mp4")
    result = instance.loop()
    assert len(result) == 3
