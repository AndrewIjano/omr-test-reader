from amc_reader.test_reader import TestReader

import os
import argparse
import json

def is_read_test_successful(test_image_filename, detector_type):
    test_code, _ = TestReader.read_test(test_image_filename, detector_type)
    return test_code.is_code_valid


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the images dataset")
    parser.add_argument("detector_type", choices=["thresholding", "log"])
    parser.add_argument("--out", required=False)
    return parser.parse_args()


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
        is_reading_sucessful = False
        try:
            is_reading_sucessful = is_read_test_successful(path + img_file, detector_type)
        except Exception as e:
            print(f' ({e}) ')
        finally:
            print(is_reading_sucessful)
            successful_reading_count += int(is_reading_sucessful)
            read_results += [{'file': img_file, 'success': is_reading_sucessful}]

    print(
        f'test reading success: {successful_reading_count}/{images_count}'
        f' ({100*successful_reading_count/images_count:4.2f}%)'
    )

    if args.out is not None:
        with open(args.out, 'w') as f:
            f.write(json.dumps(read_results))
