import cv2 
import numpy as np 
import glob  

class Camera(object):

    def __init__(self, matrix, distortion): 
        self.matrix = matrix
        self.dist = distortion

    def get_matrix(self):
        return self.__matrix

    def get_dist(self):
        return self.__dist

    def set_matrix(self, camera_matrix):
        """The camera matrix is of size 3x3 and shall contain the following information at the following indices
         [1,1] = focal length f_x
         [2,2] = focal length f_y 
         [1,3] = optical center c_x
         [2,3] = optical center c_y"""
        try: 
            if np.shape(camera_matrix) == (3,3): 
                NaN = float('nan') 
                template_matrix = np. array ([[NaN, 0, NaN], [0, NaN, NaN], [0,0,1]])
                masking_matrix = np.array ([[False, True, False], [True, False, False], [True, True, True]])
                if np.array_equal(masking_matrix,(camera_matrix == template_matrix))== True: 
                    self.__matrix = camera_matrix 
                else: 
                    raise ValueError("wrong camera_matrix")
            else: 
                raise ValueError ("camera_matrix has wrong size")
        except ValueError as v: 
            print("ValueError: ", v)

    def set_dist(self, camera_dist):
        """The array for the distortion coefficients must be of size 5x1"""
        try: 
            if np.shape(camera_dist) == (1,5): 
                self.__dist = camera_dist 
            else: 
                raise ValueError("camera_dist has wrong size")
        except ValueError as v: 
            print("ValueError: ", v)
    
    matrix = property(get_matrix, set_matrix)
    dist = property(get_dist, set_dist)

    @staticmethod
    def calibrate():
        CHECKERBOARD = (6, 9)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        threedpoints = []
        twodpoints = []

        objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
        objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

        images = glob.glob('*.jpg', recursive=True)

        for filename in images:
            global image
            image = cv2.imread(filename)
            grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners( grayColor, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH
                            + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if ret == True:
                 threedpoints.append(objectp3d)
                 corners2 = cv2.cornerSubPix(
                     grayColor, corners, (11, 11), (-1, -1), criteria)

                 twodpoints.append(corners2)
        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            threedpoints, twodpoints, grayColor.shape[::-1], None, None)

        # Displaying required output for developping purpose 
        print(" Camera matrix:")
        print(matrix)

        print("\n Distortion coefficient:")
        print(distortion)

        print("\n Rotation Vectors:")
        print(r_vecs)

        print("\n Translation Vectors:")
        print(t_vecs)

        NewCamera = Camera(matrix, distortion)
        return NewCamera
