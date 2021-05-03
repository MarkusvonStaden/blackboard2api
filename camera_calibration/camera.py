import cv2 #so far unused in this file
import numpy as np  

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

    #evtl. setter definieren, manche Felder von matrix sind ja immer 0 

#methods
pass 