import os
import sys
import shutil
from tqdm import tqdm


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

    n = int(label_num) if 0 < int(label_num) < len(os.listdir(src_label_dir)) else len(os.listdir(src_label_dir))
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


def coco_split(config):
    split_label, split_image, yolov5_dir = config['split_label'], config['split_image'], config['yolov5_dir']
    assert os.path.isdir(split_image), 'ERROR: --src image folder does not exist.'
    assert os.path.isdir(split_label), 'ERROR: --src label folder does not exist.'
    assert os.path.isdir(yolov5_dir), 'ERROR: --dst yolov5 folder does not exist.'
    assert len(os.listdir(split_image)), 'ERROR: --src image folder is empty.'
    assert len(os.listdir(split_label)), 'ERROR: --src label folder is empty.'
    # assert len(os.listdir(yolov5_dir)) == 0, 'ERROR: --dst yolov5 folder is not empty'

    train_ptg, val_ptg, test_ptg = config['ratio'][0], config['ratio'][1], config['ratio'][2]
    assert train_ptg + val_ptg + test_ptg == 1, 'ERROR: --invalid percentage.'

    train_labels = config['yolov5_train_labels']
    train_images = config['yolov5_train_images']
    valid_labels = config['yolov5_val_labels']
    valid_images = config['yolov5_val_images']
    test_labels = config['yolov5_test_labels']
    test_images = config['yolov5_test_images']
    val_num = int(val_ptg * len(os.listdir(split_label)))
    test_num = int(val_ptg * len(os.listdir(split_label)))

    print('Labels being split...')
    with tqdm(total=len(os.listdir(split_label)), file=sys.stdout) as pbar:
        for i, c in enumerate(os.listdir(split_label)):
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
