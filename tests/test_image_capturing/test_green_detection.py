from ...image_capturing.green_detection import Blackboard
import numpy as np
import cv2

image = np.zeros((1080*2, 1920*2, 3), np.float32)
empty_image = image
image[250:750, 250:1750] = np.array((60, 60, 60), np.float32)
image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)

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

def test_sort():
    points = np.array(([[[0,0]],[[0,1]],[[1,0]],[[1,1]]]))
    expected_result = np.float32([[0,0], [0,1], [1,0], [1,1]])
    result = Blackboard._sort_points(points)
    assert np.array_equal(result, expected_result)

def test_resize():
    expected_result = (1080, 1920, 3)
    result = Blackboard._resize(image, 0.5).shape
    assert result == expected_result