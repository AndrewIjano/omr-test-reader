from amc_reader.test_reader import TestReader

import os

PATH = './data/scans/'


def is_read_test_successful(test_image_filename):
    test_code, _ = TestReader.read_test(test_image_filename)
    return test_code.is_code_valid


if __name__ == '__main__':
    successful = 0
    images_count = len(os.listdir(PATH))

    for i, img_file in enumerate(sorted(os.listdir(PATH))):
        print(end=f'{i/images_count*100:4.2f}% - {img_file} ')
        try:
            result = is_read_test_successful(PATH + img_file)
            print(result)
            successful += int(result)
        except Exception as e:
            print(e)

    print(f'test reading success: {successful}/{images_count}')
