from matplotlib.pyplot import get
from amc_reader.utils import show_img
import cv2
import numpy as np

HEADER_HEIGHT = int(2840*0.0435)
TEST_WIDTH = 2840
TEST_HEIGHT = 4110 + HEADER_HEIGHT


class ImageHandler:
    @staticmethod
    def read_image(image_filename):
        return cv2.imread(image_filename)

    @staticmethod
    def filter_image(img):
        def get_kernel(d):
            return cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(d, d))

        img = cv2.GaussianBlur(img, (9, 9), 0)
        img = img.astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 99, 3)

        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, get_kernel(d=7))

        return img

    @staticmethod
    def correct_rotation(img, keypoints):
        input_pts = np.float32(keypoints)
        output_pts = np.float32(
            [[0, HEADER_HEIGHT], [TEST_WIDTH, HEADER_HEIGHT],
                [TEST_WIDTH, TEST_HEIGHT], [0, TEST_HEIGHT]]
        )

        M = cv2.getPerspectiveTransform(input_pts, output_pts)
        corrected_img = cv2.warpPerspective(
            img, M, (TEST_WIDTH, TEST_HEIGHT + HEADER_HEIGHT), flags=cv2.INTER_LINEAR
        )

        corrected_keypoints = np.array(output_pts).astype(int)

        return corrected_img, corrected_keypoints

    @staticmethod
    def rotate_image180(img):
        return np.rot90(img, k=2)
