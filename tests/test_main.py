import sys
sys.path.append("./")
import main
def test_video_returns_three_boards():
    instance = main.Main(recalibrate_camera = False, path = "test.mp4")
    result = instance.loop()
    assert len(result) == 3
