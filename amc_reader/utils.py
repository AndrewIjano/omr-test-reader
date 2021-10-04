import cv2
import numpy as np

from matplotlib import pyplot as plt

from amc_reader.code_reader import Rectangle
from amc_reader.code_reader import RelativeSpace
from skimage import color

LINE_THICKNESS = 4

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def show_debug_image(image_filename, keypoints):
    img = cv2.imread(image_filename)
    draw_keypoints(img, keypoints)

    relative_space = RelativeSpace(keypoints)
    draw_rectangle(img, relative_space.get_test_code_rectangle_1(), RED)
    draw_rectangle(img, relative_space.get_test_code_rectangle_2(), RED)
    draw_rectangle(img, relative_space.get_nusp_rectangle(), GREEN)

    show_img(img)

def show_image_with_draw(img, keypoints):
    relative_space = RelativeSpace(keypoints)
    draw_rectangle(img, relative_space.get_test_code_rectangle_1(), RED)
    draw_rectangle(img, relative_space.get_test_code_rectangle_2(), RED)
    draw_rectangle(img, relative_space.get_nusp_rectangle(), GREEN)

    show_img(img)


def draw_keypoints(debug_image, keypoints):
    n = len(keypoints)
    offset = np.array((25, -25))
    for i in range(n):
        cv2.putText(debug_image, str(
            i), keypoints[i] + offset, cv2.FONT_HERSHEY_SIMPLEX, 3, BLUE, 8)
        cv2.line(debug_image, keypoints[i], keypoints[(
            i+1) % n], BLUE, thickness=LINE_THICKNESS)


def draw_rectangle(img, rectangle: Rectangle, color):
    cv2.rectangle(img, rectangle.top_left,
                  rectangle.bot_right, color, LINE_THICKNESS)


def show_img(img):
    plt.imshow(img)
    plt.rcParams['figure.figsize'] = [200, 50]
    plt.show()

def show_img_with_blobs(img, blobs):
    d_img = np.copy(img)
    d_img = color.gray2rgb(d_img)

    _, ax = plt.subplots()
    ax.imshow(d_img)
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x, y), r, color='red', linewidth=2, fill=False)
        ax.add_patch(c)

    plt.show()