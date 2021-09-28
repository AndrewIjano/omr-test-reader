import cv2
import numpy as np


def get_keypoints(img, detector_type='thresholding'):
    detect_keypoints = get_detector(detector_type)

    keypoints = detect_keypoints(img)

    keypoints = get_sorted_keypoints(keypoints)

    if is_image_in_landscape(keypoints):
        keypoints = get_keypoints_rot90(keypoints)

    return keypoints

def get_detector(detector_type):
    return {
        'thresholding': thresholding_blob_detector
    }[detector_type]


def thresholding_blob_detector(img):
    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    # min area 180 -> scan2
    params.minArea = 480

    params.minThreshold = 0
    params.maxThreshold = 60

    params.filterByCircularity = True
    params.minCircularity = 0.87

    params.filterByConvexity = True
    params.minConvexity = 0.85

    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    detector = cv2.SimpleBlobDetector_create(params)

    cv2_keypoints = detector.detect(img)

    return np.array([k.pt for k in cv2_keypoints]).astype(int)


def log_blob_detector(img):
    keypoints = []

    return keypoints


def get_sorted_keypoints(keypoints):
    kp_sum = np.sum(keypoints, axis=1)
    kp_dif = np.diff(keypoints, axis=1)

    return keypoints[[
        np.argmin(kp_sum),
        np.argmin(kp_dif),
        np.argmax(kp_sum),
        np.argmax(kp_dif),
    ]]

def is_image_in_landscape(keypoints):
    m1, m2, _, m4 = keypoints
    width = np.linalg.norm(m1 - m2)
    height = np.linalg.norm(m1 - m4)
    return width > height

def get_keypoints_rot90(keypoints):
    return keypoints[[1, 2, 3, 0]]