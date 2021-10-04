from amc_reader.test_reader import TestReader

import os
import argparse


def is_read_test_successful(test_image_filename, detector_type):
    test_code, _ = TestReader.read_test(test_image_filename, detector_type)
    return test_code.is_code_valid


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the images dataset")
    parser.add_argument("detector_type", choices=["thresholding", "log"])
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    path = args.path
    detector_type = args.detector_type

    successful_reading_count = 0
    images_files = sorted(os.listdir(path))
    images_count = len(images_files)

    for i, img_file in enumerate(images_files):
        print(end=f'{i/images_count*100:4.2f}% - {img_file} ')
        try:
            result = is_read_test_successful(path + img_file, detector_type)
            print(result)
            successful_reading_count += int(result)
        except Exception as e:
            print(e)

    print(f'test reading success: {successful_reading_count}/{images_count}')
