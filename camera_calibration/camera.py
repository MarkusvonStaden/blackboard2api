import cv2 #so far unused in this file 

# definition of the class Camera
# 
class Camera(object):
#todo: entscheiden ob private/public/property etc. 

    def __init__(self): 
        self.matrix = np.zeros(3,3)     #camera matrix
        self.dist = np.zeros(5,1)       #distortion coefficients

    #evtl. setter definieren, manche Felder von matrix sind ja immer 0 

#methods
pass 