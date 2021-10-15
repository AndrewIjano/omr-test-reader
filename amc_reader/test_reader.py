from amc_reader.utils import show_debug_image
from amc_reader.image_handler import read_image, filter_image, correct_rotation, rotate_image180
from amc_reader.keypoints_detector import get_keypoints
from amc_reader.test_code_reader import get_test_code
from amc_reader.nusp_code_reader import get_nusp_code


def read_test(test_image_filename, detector_type, debug=False):
    img = read_image(test_image_filename)
    img = filter_image(img)

    keypoints = get_keypoints(img, detector_type)

    if debug:
        show_debug_image(test_image_filename, keypoints)

    img, keypoints = correct_rotation(img, keypoints)

    test_code = get_test_code(img, keypoints)

    if not test_code.is_code_valid:
        img = rotate_image180(img)
        test_code = get_test_code(img, keypoints)

    nusp_code = (
        get_nusp_code(img, keypoints)
        if test_code.test_page == 1
        else None
    )
    return test_code, nusp_code
