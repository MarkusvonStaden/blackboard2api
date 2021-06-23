import sys
sys.path.append("./")
import main
def test_video_returns_three_boards():
    """
    test whether three boards can be found in the test video 
    """
    instance = main.Main(recalibrate_camera = False, path = "tests/Compressed_Test.mp4")
    result = instance.loop()
    assert len(result) == 3
