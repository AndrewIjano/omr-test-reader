'''
    Makes the experiment for a given dataset and detector
'''

from amc_reader.image_handler import read_image
from amc_reader import test_reader 

import os
import argparse
import json
import time


def is_read_test_successful(test_image_filename, detector_type):
    test_code, _ = test_reader.read_test(test_image_filename, detector_type)
    return test_code.is_code_valid


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the images dataset")
    parser.add_argument("detector_type", choices=["simple", "doh"])
    parser.add_argument("--out", required=False)
    return parser.parse_args()


def get_pixels_from_image(img_path):
    img = read_image(img_path)
    x, y, _ = img.shape
    return x*y


if __name__ == '__main__':
    args = get_args()
    path = args.path
    detector_type = args.detector_type

    successful_reading_count = 0
    images_files = sorted(os.listdir(path))
    images_count = len(images_files)

    read_results = []
    for i, img_file in enumerate(images_files):
        print(end=f'{i/images_count*100:5.2f}% - {img_file} ')
        img_path = path + img_file
        is_reading_sucessful = False
        pixels = get_pixels_from_image(img_path)
        start_time = time.time()
        try:
            is_reading_sucessful = is_read_test_successful(
                img_path, detector_type)
        except Exception as e:
            print(f' ({e}) ')
        finally:
            print(is_reading_sucessful)
            successful_reading_count += int(is_reading_sucessful)
            read_results += [{'file': img_file, 'success': is_reading_sucessful,
                              'time': time.time() - start_time, 'pixels': pixels}]

    print(
        f'test reading success: {successful_reading_count}/{images_count}'
        f' ({100*successful_reading_count/images_count:4.2f}%)'
    )

    if args.out is not None:
        with open(args.out, 'w') as f:
            f.write(json.dumps(read_results))
