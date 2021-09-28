
import cv2
import numpy as np
import collections

Rectangle = collections.namedtuple('Rectangle', ['top_left', 'bot_right'])


class TestCode:
    def __init__(self, test_number: int, test_page: int, verification_code: int) -> None:
        self.test_number = test_number
        self.test_page = test_page
        self.verification_code = verification_code

    @property
    def is_code_valid(self):
        expected_number = 60 - ((self.test_number - 1)
                                * 4 + (self.test_page - 1)) % 60
        return expected_number == self.verification_code


class RelativeSpace:
    def __init__(self, keypoints) -> None:
        self.w, self.m1 = self.get_w_m1(keypoints)

    @staticmethod
    def get_w_m1(keypoints):
        m1, m2, *_ = keypoints
        w = np.linalg.norm(m1 - m2)
        return w, m1

    def get_nusp_rectangle(self):
        return Rectangle(
            self.get_relative_point(0.0456, 0.111),
            self.get_relative_point(0.2484, 0.4049)
        )

    def get_test_code_rectangle_1(self):
        return Rectangle(
            self.get_relative_point(0.259, -0.0435),
            self.get_relative_point(0.474, -0.0258)
        )

    def get_test_code_rectangle_2(self):
        return Rectangle(
            self.get_relative_point(0.259, -0.0208),
            self.get_relative_point(0.474, -0.0032)
        )

    def get_relative_point(self, x, y):
        return (self.w * np.array((x, y)) + self.m1).astype(int)


TEST_CODE_SQUARE_COUNT = 12
WHITE_RATIO_THRESHOLD = 0.4


class TestCodeReader:
    def __init__(self, img, keypoints):
        self.img = img
        self.keypoints = keypoints

    def get_test_code(self) -> TestCode:
        relative_space = RelativeSpace(self.keypoints)

        rectangle_1 = relative_space.get_test_code_rectangle_1()
        rectangle_2 = relative_space.get_test_code_rectangle_2()

        raw_code_1 = self.get_rectangle_code(rectangle_1)
        raw_code_2 = self.get_rectangle_code(rectangle_2)

        test_number = int(raw_code_1, base=2)
        test_page = int(raw_code_2[:TEST_CODE_SQUARE_COUNT//2], base=2)
        verification_code = int(raw_code_2[TEST_CODE_SQUARE_COUNT//2:], base=2)

        return TestCode(test_number, test_page, verification_code)

    def get_rectangle_code(self, rectangle: Rectangle) -> str:
        x0, y0 = rectangle.top_left
        x1, y1 = rectangle.bot_right

        rectangle_width = x1 - x0
        rectangle_width -= rectangle_width % TEST_CODE_SQUARE_COUNT
        square_width = rectangle_width // TEST_CODE_SQUARE_COUNT
        square_white = square_width**2

        rectangle_img = self.img[y0:y1, x0:x1]

        rectangle_code = []

        for x in range(0, rectangle_width, square_width):
            square_img = rectangle_img[0:square_width, x:x+square_width]

            total_white = cv2.countNonZero(square_img)
            is_filled = total_white / square_white < WHITE_RATIO_THRESHOLD
            rectangle_code += [str(int(is_filled))]

        return ''.join(rectangle_code)


NUSP_SQUARE_COUNT = 8
NUSP_DIGIT_COUNT = 10


class NuspCodeReader:
    def __init__(self, img, keypoints):
        self.img = img
        self.keypoints = keypoints

    def get_nusp_code(self):
        relative_space = RelativeSpace(self.keypoints)
        nusp_rectangle = relative_space.get_nusp_rectangle()

        x0, y0 = nusp_rectangle.top_left
        x1, y1 = nusp_rectangle.bot_right

        rectangle_img = self.img[y0:y1, x0:x1]

        rectangle_img = self.remove_numbers(rectangle_img)

        rectangle_width = int(x1 - x0)
        rectangle_height = int(y1 - y0)

        square_width = int((0.9*rectangle_width) // NUSP_SQUARE_COUNT)
        nusp_vertical_space = self.get_space_between(
            rectangle_height, square_width, NUSP_DIGIT_COUNT)
        nusp_horizontal_space = self.get_space_between(
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
            digit, min_ratio = min(
                enumerate(white_ratios),
                key=lambda digit_ratio: digit_ratio[1]
            )
            return str(digit)

        nusp_code = ''.join(
            get_nusp_digit(digit_position)
            for digit_position in range(NUSP_SQUARE_COUNT)
        )

        return nusp_code

    @staticmethod
    def get_space_between(total_length, element_length, elements_count):
        return int((total_length - elements_count * element_length) // (elements_count - 1))

    @staticmethod
    def remove_numbers(img):
        def get_kernel(d):
            return cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(d, d))

        img = cv2.dilate(img, get_kernel(d=4))
        img = cv2.erode(img, get_kernel(d=7))
        return img
