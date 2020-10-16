import argparse
import utils


def generate():
    utils.coco_dataset_filter(lnum=opt.n, config=opt.cfg)
    # utils.test()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--net', type=str, default='yolov3', help='[yolov3, yolov5]')
    parser.add_argument('--n', type=str, default='-1', help='num of labels selected')
    parser.add_argument('--cfg', type=str, default='.\\config.yaml', help='config yaml folder')

    opt = parser.parse_args()

    generate()
