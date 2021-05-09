import cv2 
import numpy as np 
import os
import glob  

# definition of the class Camera
# 
class Camera(object):
#todo: entscheiden ob private/public/property etc. 

    def __init__(self): 
        self.__matrix = np.zeros((3,3))     #camera matrix
        self.__dist = np.zeros((5,1))      #distortion coefficients

    def get_matrix(self):
        return self.__matrix
    def get_dist(self):
        return self.__dist
    def set_matrix(self, camera_matrix):
        # The camera matrix is of size 3x3 and shall contain the following information at the following indices
        # [1,1] = focal length f_x
        # [2,2] = focal length f_y 
        # [1,3] = optical center c_x
        # [2,3] = optical center c_y
        if np.shape(camera_matrix) == (3,3): 
            NaN = float('nan') 
            template_matrix = np. array ([[NaN, 0, NaN], [0, NaN, NaN], [0,0,1]])
            masking_matrix = np.array ([[False, True, False], [True, False, False], [True, True, True]])
            if np.array_equal(masking_matrix,(camera_matrix == template_matrix))== True: 
                self.__matrix = camera_matrix 
    def set_dist(self, camera_dist):
        # The array for the distortion coefficients must be of size 5x1
        if np.shape(camera_dist) == (5,1): 
            self.__dist = camera_dist 
    
    matrix = property(get_matrix, set_matrix)
    dist = property(get_dist, set_dist)

    @staticmethod
    def calibrate():

        # Define the dimensions of checkerboard
        CHECKERBOARD = (6, 9)

        # stop the iteration when specified accuracy, epsilon, is reached or specified number of iterations are completed.
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Vector for 3D points
        threedpoints = []

        # Vector for 2D points
        twodpoints = []

        # 3D points real world coordinates
        objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
        objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
        prev_img_shape = None

        # Extracting path of individual image stored in a given directory. 
        # Since no path is specified, it will take current directory jpg files alone
        images = glob.glob('*.jpg', recursive=True)
        #print(images)

        for filename in images:
            global image
            image = cv2.imread(filename)
            grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            # If desired number of corners are found in the image then ret = true
            ret, corners = cv2.findChessboardCorners( grayColor, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH
                            + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

            # If desired number of corners can be detected then, 
            # refine the pixel coordinates and display them on the images of checker board
            # if ret == True:
            #     threedpoints.append(objectp3d)

            #     # Refining pixel coordinates
            #     # for given 2d points.
            #     corners2 = cv2.cornerSubPix(
            #         grayColor, corners, (11, 11), (-1, -1), criteria)

            #     twodpoints.append(corners2)

            #     # Draw and display the corners
            #     image = cv2.drawChessboardCorners(image,
            #                                     CHECKERBOARD,
            #                                     corners2, ret)

            cv2.imshow('img', image)
            cv2.waitKey(0)

        cv2.destroyAllWindows()

        h, w = image.shape[:2]


        # Perform camera calibration by
        # passing the value of above found out 3D points (threedpoints)
        # and its corresponding pixel coordinates of the
        # detected corners (twodpoints)
        #ret = return value 
        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            threedpoints, twodpoints, grayColor.shape[::-1], None, None)

        # Save attributes in an object
        # todo: anpassen, da es jetzt eine Methode ist!! 
        CurrentCamera = ca.Camera()
        CurrentCamera.set_matrix(matrix)
        CurrentCamera.set_dist(distortion)

        # Displaying required output
        print(" Camera matrix:")
        print(matrix)

        print("\n Distortion coefficient:")
        print(distortion)

        print("\n Rotation Vectors:")
        print(r_vecs)

        print("\n Translation Vectors:")
        print(t_vecs)

        #for developping purpose
        print("\n Camera matrix in CurrentCamera")
        print(CurrentCamera.get_matrix())

        print("\n Distortion coefficients in CurrentCamera")
        print(CurrentCamera.get_dist())


#methods
pass 