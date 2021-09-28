import argparse

from amc_reader.code_reader import TestCode
from amc_reader.test_reader import TestReader


def show_result(test_code: TestCode, nusp_code: str):
    print('Successful detection:')
    print(f'test number: {test_code.test_number}')
    print(f'page: {test_code.test_page} code: {test_code.verification_code}')
    print(f'nusp: {nusp_code}')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("test_image_filename", help="test image filename")
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    test_code, nusp_code = TestReader.read_test(args.test_image_filename)
    show_result(test_code, nusp_code)
