from amc_reader.models import RelativeSpace

import cv2

NUSP_SQUARE_COUNT = 8
NUSP_DIGIT_COUNT = 10


def get_nusp_code(img, keypoints) -> str:
    relative_space = RelativeSpace(keypoints)
    nusp_rectangle = relative_space.get_nusp_rectangle()

    x0, y0 = nusp_rectangle.top_left
    x1, y1 = nusp_rectangle.bot_right

    rectangle_img = img[y0:y1, x0:x1]

    rectangle_img = remove_numbers(rectangle_img)

    rectangle_width = int(x1 - x0)
    rectangle_height = int(y1 - y0)

    square_width = int((0.9*rectangle_width) // NUSP_SQUARE_COUNT)
    nusp_vertical_space = get_space_between(
        rectangle_height, square_width, NUSP_DIGIT_COUNT)
    nusp_horizontal_space = get_space_between(
        rectangle_width, square_width, NUSP_SQUARE_COUNT)

    square_all_white = square_width**2

    def get_nusp_column_white_ratios(digit_position):
        x = (square_width + nusp_horizontal_space)*digit_position
        for y in range(0, rectangle_height, square_width + nusp_vertical_space):
            square_img = rectangle_img[y:y+square_width, x:x+square_width]
            square_white_count = cv2.countNonZero(square_img)
            yield square_white_count / square_all_white

    def get_nusp_digit(digit_position):
        white_ratios = get_nusp_column_white_ratios(digit_position)
        digit, _ = min(enumerate(white_ratios),
                       key=lambda digit_ratio: digit_ratio[1])
        return str(digit)

    nusp_code = ''.join(
        get_nusp_digit(digit_position)
        for digit_position in range(NUSP_SQUARE_COUNT)
    )

    return nusp_code


def get_space_between(total_length, element_length, elements_count):
    return int((total_length - elements_count * element_length) // (elements_count - 1))


def remove_numbers(img):
    def get_kernel(d):
        return cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(d, d))

    img = cv2.dilate(img, get_kernel(d=4))
    img = cv2.erode(img, get_kernel(d=7))
    return img
