
from amc_reader.utils import show_debug_image, show_image_with_draw, show_img
from amc_reader.image_handler import ImageHandler
from amc_reader.keypoints_detector import get_keypoints
from amc_reader.code_reader import TestCodeReader, NuspCodeReader


class TestReader:
    @staticmethod
    def read_test(test_image_filename, detector_type, debug=False):
        img = ImageHandler.read_image(test_image_filename)
        img = ImageHandler.filter_image(img)

        keypoints = get_keypoints(img, detector_type)

        if debug:
            show_debug_image(test_image_filename, keypoints)

        img, keypoints = ImageHandler.correct_rotation(img, keypoints)

        test_code = TestCodeReader(img, keypoints).get_test_code()

        if not test_code.is_code_valid:
            img = ImageHandler.rotate_image180(img)
            test_code = TestCodeReader(img, keypoints).get_test_code()

        nusp_code = (
            NuspCodeReader(img, keypoints).get_nusp_code()
            if test_code.test_page == 1
            else None
        )
        return test_code, nusp_code
