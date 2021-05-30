from ...image_capturing.green_detection import Blackboard
import numpy as np
import cv2

image = np.ones((1080*2, 1920*2, 3), np.uint8) * 255.0
empty_image = image
image[250:750, 250:1750] = np.array((0,1,0), np.uint8)*255

def test_blackboard_detection():
    blackboard = Blackboard.from_image(image)
    assert type(blackboard) is Blackboard
    assert blackboard.contour is not None
    assert blackboard.board is not None 

def test_blackboard_detection_with_empty_image():
    blackboard = Blackboard.from_image(empty_image)
    assert type(blackboard) is Blackboard
    assert blackboard.contour is None
    assert blackboard.board is None 