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
