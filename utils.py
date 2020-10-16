import os
import shutil
import yaml


def filter_label(slabel, dlabel, lnum):
    assert os.path.isdir(slabel), 'ERROR: --label folder does not exist'
    assert len(os.listdir(slabel)), 'ERROR: --label folder is empty'
    assert os.path.isdir(dlabel), 'ERROR: --dest label folder does not exist'
    assert len(os.listdir(dlabel)) == 0, 'ERROR: --dest label folder is not empty'

    clist = ['0']

    n = int(lnum) if 0 < int(lnum) < len(os.listdir(slabel)) else len(os.listdir(slabel))

    for filename in os.listdir(slabel):
        if n == 0:
            break

        with open(os.path.join(slabel, filename), 'r') as f:
            lines = f.readlines()

        new_lines = [line for line in lines if line.strip('\n')[0] in clist]

        if len(new_lines):
            with open(os.path.join(dlabel, filename), 'w') as f:
                for line in new_lines:
                    f.write(line)
            n -= 1

    return dlabel


def filter_img(simage, slabel, dimage):
    assert os.path.isdir(simage), 'ERROR: --image folder does not exist'
    assert os.path.isdir(dimage), 'ERROR: --image dest folder does not exist'
    assert len(os.listdir(dimage)) == 0, 'ERROR: --dest image folder is not empty'

    for label_name in os.listdir(slabel):
        image_name = os.path.splitext(label_name)[0] + '.jpg'
        try:
            shutil.copyfile(os.path.join(simage, image_name), os.path.join(dimage, image_name))
        except RuntimeError:
            print('RuntimeError: copy image failed')
            raise

