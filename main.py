import argparse
import utils
import yaml


def generate():
    config = yaml.load(open(opt.cfg), Loader=yaml.FullLoader)

    if opt.do == 'filter':
        utils.coco_dataset_filter(lnum=opt.n, config=config)
    if opt.do == 'split':
        utils.coco_split(config=config)
    if opt.do == 'concat':
        utils.concat_label(config=config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--do', type=str, default='filter', help='[filter, split, yolov3, yolov5]')
    parser.add_argument('--n', type=str, default='-1', help='num of labels selected')
    parser.add_argument('--cfg', type=str, default='.\\config.yaml', help='config yaml folder')

    opt = parser.parse_args()

    generate()
    # # python main.py --do filter --n 1000
