from glob import glob
import cv2 
import numpy as np 
import pickle
from dataclasses import dataclass

@dataclass(frozen = True)       
class DistortionCamera:
    cameramatrix: np.ndarray
    roi: tuple
    matrix: np.ndarray
    dist: np.ndarray

    def __post_init__(self):
        """ Acts as init-method for a dataclass. 
        """
        if np.shape(self.matrix) != (3,3): raise ValueError("wrong matrix shape")

    def __save_obj(self, pathname):
        """ Saves the object with the information about camera-specific distortion
        """
        CurrentCameraFile = open(pathname, "wb")
        pickle.dump(self, CurrentCameraFile)

    @classmethod
    def create_camera_matrix_from_images(cls, images: tuple, pathname: str):
        """ Calculates the camera matrix from reference images.
        Images must be photos of a chessboard with 6 x 9 fields photographed from different angles. 
        """
        CHECKERBOARD = (6, 9)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        threedpoints = []
        twodpoints = []

        objectp3d = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
        objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

        for image in images:

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK 
            + cv2.CALIB_CB_NORMALIZE_IMAGE)
            if not ret:
                raise ValueError("Error getting corners")

            threedpoints.append(objectp3d)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            twodpoints.append(corners2)
            
        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(threedpoints, twodpoints, (1920*2, 1080*2), None, None)

        if not ret:
            raise ValueError("Error getting optimal camera matrix")

        cameramtx, roi = cv2.getOptimalNewCameraMatrix(matrix, distortion, (1920*2, 1080*2), None, None)

        CurrentCamera = cls(cameramtx, roi, matrix, distortion)
        CurrentCamera.__save_obj(pathname)

        return CurrentCamera

    @classmethod
    def create_camera_matrix_from_directory(cls, path: str, filetype: str, filename: str):
        """ Calls create_camera_matrix_from_images with images from the directory. 
        """
        filenames = glob(path+"*"+filetype, recursive=True)
        images = [cv2.imread(filename) for filename in filenames]
        if len(images) > 0:
            return cls.create_camera_matrix_from_images(images, filename)
        else:
            raise NameError("Image path does not exist")

    @staticmethod
    def create_matrix_from_file(pathname: str):
        """ Creates a camera matrix as an instance of DistortionCamera from a binary file. 
        """
        camera_file = open(pathname, "rb")
        instance = pickle.load(camera_file)
        if type(instance) == DistortionCamera: return instance

    def undistort_image(self, image):
        """ Eliminates camera dependent distortion in an image. 
        """
        dst = cv2.undistort(image, self.matrix, self.dist, None, self.cameramatrix)
        x, y, w, h = self.roi
        return dst[y:y+h, x:x+w]