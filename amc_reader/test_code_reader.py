from amc_reader.models import TestCode, RelativeSpace, Rectangle

import cv2

TEST_CODE_SQUARE_COUNT = 12
WHITE_RATIO_THRESHOLD = 0.4


def get_test_code(img, keypoints) -> TestCode:
    relative_space = RelativeSpace(keypoints)

    rectangle_1 = relative_space.get_test_code_rectangle_1()
    rectangle_2 = relative_space.get_test_code_rectangle_2()

    raw_code_1 = get_rectangle_code(img, rectangle_1)
    raw_code_2 = get_rectangle_code(img, rectangle_2)

    raw_code_2_1 = raw_code_2[:TEST_CODE_SQUARE_COUNT//2]
    raw_code_2_2 = raw_code_2[TEST_CODE_SQUARE_COUNT//2:]

    test_number = get_number(raw_code_1)
    test_page = get_number(raw_code_2_1)
    verification_code = get_number(raw_code_2_2)

    return TestCode(test_number, test_page, verification_code)


def get_rectangle_code(img, rectangle: Rectangle) -> str:
    x0, y0 = rectangle.top_left
    x1, y1 = rectangle.bot_right

    rectangle_width = x1 - x0
    rectangle_width -= rectangle_width % TEST_CODE_SQUARE_COUNT
    square_width = rectangle_width // TEST_CODE_SQUARE_COUNT
    square_white = square_width**2

    rectangle_img = img[y0:y1, x0:x1]

    rectangle_code = []

    for x in range(0, rectangle_width, square_width):
        square_img = rectangle_img[0:square_width, x:x+square_width]

        total_white = cv2.countNonZero(square_img)
        is_filled = total_white / square_white < WHITE_RATIO_THRESHOLD
        rectangle_code += [str(int(is_filled))]

    return ''.join(rectangle_code)


def get_number(binary_int: str) -> int:
    return int(binary_int, base=2)
