import os
import sys
import shutil
import yaml
from tqdm import tqdm


# # from a full coco dataset, including images and labels, to a class-filtered coco dataset
def filter_label(slabel, dlabel, lnum, clist):
    assert os.path.isdir(slabel), 'ERROR: --label folder does not exist'
    assert len(os.listdir(slabel)), 'ERROR: --label folder is empty'
    assert os.path.isdir(dlabel), 'ERROR: --dest label folder does not exist'
    assert len(os.listdir(dlabel)) == 0, 'ERROR: --dest label folder is not empty'

    n = int(lnum) if 0 < int(lnum) < len(os.listdir(slabel)) else len(os.listdir(slabel))

    print('Labels being selected...')
    with tqdm(total=n, file=sys.stdout) as pbar:
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

            pbar.update(1)
    return dlabel


def filter_img(simage, slabel, dimage):
    assert os.path.isdir(simage), 'ERROR: --image folder does not exist'
    assert os.path.isdir(dimage), 'ERROR: --image dest folder does not exist'
    assert len(os.listdir(dimage)) == 0, 'ERROR: --dest image folder is not empty'

    print('Images being selected...')
    with tqdm(total=len(os.listdir(slabel)), file=sys.stdout) as pbar:
        for label_name in os.listdir(slabel):
            image_name = os.path.splitext(label_name)[0] + '.jpg'
            try:
                shutil.copyfile(os.path.join(simage, image_name), os.path.join(dimage, image_name))
            except RuntimeError:
                print('RuntimeError: copy image failed')
                raise

            pbar.update(1)


def coco_dataset_filter(lnum, config):
    config = open(config)
    parsed_config = yaml.load(config, Loader=yaml.FullLoader)

    clist = parsed_config['class']
    slabel = parsed_config['src_label']
    dlabel = parsed_config['dst_label']
    simage = parsed_config['src_image']
    dimage = parsed_config['dst_image']

    filter_label(slabel=slabel, dlabel=dlabel, lnum=lnum, clist=clist)
    filter_img(simage=simage, slabel=dlabel, dimage=dimage)


# # from labelbox json to coco dataset
def labelbox(js, dlabel):
    pass

def test():
    with tqdm(total=10000000, file=sys.stdout) as pbar:
        for i in range(100):
            pbar.update(1)