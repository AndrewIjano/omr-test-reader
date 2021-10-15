'''
    Reads the codes of a given test
'''

import argparse

from amc_reader.models import TestCode
from amc_reader import test_reader


def show_result(test_code: TestCode, nusp_code: str):
    if test_code.is_code_valid:
        print('Successful detection:')
    else:
        print('Unsucessful detection!')
    print(f'test number: {test_code.test_number}')
    print(f'page: {test_code.test_page} code: {test_code.verification_code}')
    print(f'nusp: {nusp_code}')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_image_filename", help="test image filename")
    parser.add_argument("--detector", choices=["simple", "doh"],
                        default="simple", help="method used to detect keypoints")
    parser.add_argument("--debug", action="store_true", help="show debug info")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    test_code, nusp_code = test_reader.read_test(
        args.test_image_filename, args.detector, debug=args.debug)
    show_result(test_code, nusp_code)
