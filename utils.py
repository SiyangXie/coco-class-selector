import os
import sys
import shutil
from tqdm import tqdm
import random


# # from a full coco a filtered dataset
def filter_label(src_label_dir, dst_label_dir, label_num, class_list):
    assert os.path.exists(src_label_dir), 'ERROR: --source label folder does not exist.'
    assert len(os.listdir(src_label_dir)), 'ERROR: --source label folder is empty.'

    if not os.path.exists(dst_label_dir):
        os.makedirs(dst_label_dir)
        print('Dst label dir created.')
    else:
        shutil.rmtree(dst_label_dir)
        os.makedirs(dst_label_dir)
        print('Dst label dir cleared.')

    if 0 < int(label_num) < len(os.listdir(src_label_dir)):
        n = int(label_num)
        full_len = False
    else:
        n = len(os.listdir(src_label_dir))
        full_len = True

    print('Labels being selected...')

    with tqdm(total=n, file=sys.stdout) as pbar:
        for filename in os.listdir(src_label_dir):
            if n == 0:
                break

            with open(os.path.join(src_label_dir, filename), 'r') as f:
                lines = f.readlines()

            new_lines = [line for line in lines if line.strip('\n')[0] in class_list]

            if len(new_lines):
                with open(os.path.join(dst_label_dir, filename), 'w') as f:
                    for line in new_lines:
                        f.write(line)
                n -= 1
                if not full_len:
                    pbar.update(1)

            if full_len:
                pbar.update(1)

    return dst_label_dir


def filter_img(src_image_dir, src_label_dir, dst_image_dir):
    assert os.path.exists(src_image_dir), 'ERROR: --source image folder does not exist.'

    if not os.path.exists(dst_image_dir):
        os.makedirs(dst_image_dir)
        print('Dst image dir created.')
    else:
        shutil.rmtree(dst_image_dir)
        os.makedirs(dst_image_dir)
        print('Dst image dir cleared.')

    print('Images being moved...')
    with tqdm(total=len(os.listdir(src_label_dir)), file=sys.stdout) as pbar:
        for label_name in os.listdir(src_label_dir):
            image_name = os.path.splitext(label_name)[0] + '.jpg'
            try:
                shutil.copyfile(os.path.join(src_image_dir, image_name), os.path.join(dst_image_dir, image_name))
            except RuntimeError:
                print('RuntimeError: Failed to copy images.')
                raise
            pbar.update(1)


def coco_filter(label_num, config):
    class_list = config['class']

    src_label_dir, dst_label_dir, src_image_dir, dst_image_dir = \
        config['src_label'], config['dst_label'], config['src_image'], config['dst_image']

    filter_label(src_label_dir=src_label_dir, dst_label_dir=dst_label_dir, label_num=label_num, class_list=class_list)
    filter_img(src_image_dir=src_image_dir, src_label_dir=dst_label_dir, dst_image_dir=dst_image_dir)
    print('Finished.')


def label_match_image(config):
    image_dir, label_dir = config['match_image_dir'], config['match_label_dir']
    with tqdm(total=abs(len(os.listdir(label_dir)) - len(os.listdir(image_dir))), file=sys.stdout) as pbar:
        for label_name in os.listdir(label_dir):
            image_name = os.path.splitext(label_name)[0] + '.jpg'
            if not os.path.exists(os.path.join(image_dir, image_name)):
                os.remove(os.path.join(label_dir, label_name))
                pbar.update(1)
    print('Finished.')


def coco_split(config):
    split_label, split_image, train_ptg, val_ptg, test_ptg, yolov5 = \
        config['split_label'], config['split_image'], config['ratio'][0], \
        config['ratio'][1], config['ratio'][2], config['split_yolov5']

    assert train_ptg + val_ptg + test_ptg == 1, 'ERROR: --invalid percentage.'

    if not os.path.exists(yolov5):
        os.makedirs(yolov5)
        print('yolov5 dir created.')
    else:
        shutil.rmtree(yolov5)
        os.makedirs(yolov5)
        print('yolov5 dir cleared.')

    cwd = yolov5
    os.makedirs(cwd + '\\train')
    os.makedirs(cwd + '\\train\\images')
    os.makedirs(cwd + '\\train\\labels')

    os.makedirs(cwd + '\\test')
    os.makedirs(cwd + '\\test\\images')
    os.makedirs(cwd + '\\test\\labels')

    os.makedirs(cwd + '\\valid')
    os.makedirs(cwd + '\\valid\\images')
    os.makedirs(cwd + '\\valid\\labels')

    train_labels = cwd + '\\train\\labels'
    train_images = cwd + '\\train\\images'
    valid_labels = cwd + '\\valid\\labels'
    valid_images = cwd + '\\valid\\images'
    test_labels = cwd + '\\test\\labels'
    test_images = cwd + '\\test\\images'
    val_num = int(val_ptg * len(os.listdir(split_label)))
    test_num = int(val_ptg * len(os.listdir(split_label)))

    print('Shuffling...')
    split = os.listdir(split_label)
    random.shuffle(split)

    print('Labels being split...')
    with tqdm(total=len(split), file=sys.stdout) as pbar:
        for i, c in enumerate(split):
            if i < val_num:
                shutil.copyfile(os.path.join(split_label, c), os.path.join(valid_labels, c))  # copy and move file
            elif i < val_num + test_num:
                shutil.copyfile(os.path.join(split_label, c), os.path.join(test_labels, c))
            else:
                shutil.copyfile(os.path.join(split_label, c), os.path.join(train_labels, c))

            pbar.update(1)

    print('Valid images being split...')
    with tqdm(total=len(os.listdir(valid_labels)), file=sys.stdout) as pbar:
        for label_name in os.listdir(valid_labels):
            image_name = os.path.splitext(label_name)[0] + '.jpg'
            try:
                shutil.copyfile(os.path.join(split_image, image_name), os.path.join(valid_images, image_name))
                pbar.update(1)
            except RuntimeError:
                print('RuntimeError: Failed to copy images.')
                raise

    print('Test images being split...')
    with tqdm(total=len(os.listdir(test_labels)), file=sys.stdout) as pbar:
        for label_name in os.listdir(test_labels):
            image_name = os.path.splitext(label_name)[0] + '.jpg'
            try:
                shutil.copyfile(os.path.join(split_image, image_name), os.path.join(test_images, image_name))
                pbar.update(1)
            except RuntimeError:
                print('RuntimeError: Failed to copy images.')
                raise

    print('Train images being split...')
    with tqdm(total=len(os.listdir(train_labels)), file=sys.stdout) as pbar:
        for label_name in os.listdir(train_labels):
            image_name = os.path.splitext(label_name)[0] + '.jpg'
            try:
                shutil.copyfile(os.path.join(split_image, image_name), os.path.join(train_images, image_name))
                pbar.update(1)
            except RuntimeError:
                print('RuntimeError: Failed to copy images.')
                raise

    print('Finished.')


# under dev
def concat_label(config):
    slabel_dir, dlabel_dir, clist = config['slabel_dir'], config['dlabel_dir'], config['class']

    with tqdm(total=len(slabel_dir), file=sys.stdout) as pbar:
        for label_file in os.listdir(slabel_dir):

            with open(os.path.join(slabel_dir, label_file), 'r') as f:
                lines = f.readlines()

            new_lines = [line for line in lines if line.strip('\n')[0] in clist]

            if len(new_lines):
                with open(os.path.join(dlabel_dir, label_file), 'a+') as f:
                    if len(new_lines):
                        for line in new_lines:
                            f.write(line)
            pbar.update(1)


def rename(config):
    src_image_dir = config['rename_dir']
    with tqdm(total=len(src_image_dir), file=sys.stdout) as pbar:
        n = 1
        for image_file in os.listdir(src_image_dir):
            os.rename(os.path.join(src_image_dir, image_file), os.path.join(src_image_dir, 'tmp' + str(n) + '.jpg'))
            n += 1
            pbar.update(1)

    with tqdm(total=len(src_image_dir), file=sys.stdout) as pbar:
        n = 1
        for image_file in os.listdir(src_image_dir):
            os.rename(os.path.join(src_image_dir, image_file), os.path.join(src_image_dir, 'helmet' + str(n) + '.jpg'))
            n += 1
            pbar.update(1)
